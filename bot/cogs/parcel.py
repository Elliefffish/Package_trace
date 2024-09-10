import logging
from concurrent.futures import ThreadPoolExecutor

from discord import Embed, File, app_commands
from discord.app_commands import Choice
from discord.ext import commands, tasks
from parcel_tw import Platform as PlatformEnum
from parcel_tw import TrackingInfo, track

from ..configs.platform_config import platform_to_enum, platform_to_id
from ..models import Database, ParcelTable, PlatformTable, SubscriptionTable


class Parcel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_subscriptions.start()

    @commands.command("parcel")
    async def parcel(self, ctx):
        await ctx.send("Parcel command works!")

    @commands.hybrid_command("track")
    @app_commands.choices(
        platform=[
            Choice(name="7-11", value="7-11"),
            Choice(name="全家", value="family"),
            Choice(name="OK", value="ok"),
            Choice(name="蝦皮", value="shopee"),
        ]
    )
    async def track_status(
        self, ctx, platform: str | None = None, order_id: str | None = None
    ):
        if not platform or not order_id:
            await ctx.send("參數輸入有錯誤喔！")
            return

        # Check if platform is valid
        platform = platform.lower()
        if platform not in platform_to_enum:
            await ctx.send("查不到這個物流平台!")
            return

        platform_enum = platform_to_enum[platform]
        result = track(platform_enum, order_id)

        if result is None:
            await ctx.send("No result found")
        else:
            user_id = ctx.author.id
            file_name = self._get_image_name(result.platform)
            embed = self._generate_embed(result, file_name)
            file = File(f"bot/static/img/{file_name}", filename=f"{file_name}")

            await ctx.send(f"<@{user_id}>", embed=embed, file=file)

    @commands.hybrid_command("subscribe", description="訂閱物流狀態")
    @app_commands.describe(platform="物流平台", order_id="取貨編號")
    @app_commands.choices(
        platform=[
            Choice(name="7-11", value=1),
            Choice(name="全家", value=2),
            Choice(name="OK", value=3),
            Choice(name="蝦皮", value=4),
        ]
    )
    async def subscribe(self, ctx, platform: int, order_id: str):
        user_id = ctx.author.id

        try:
            with Database() as db:
                subscription_table = SubscriptionTable(db)

                # Check if user is already subscribed
                subscription = subscription_table.get(user_id, order_id, platform)
                if subscription:
                    await ctx.send("已經訂閱過了！")
                    return

                # Insert subscription
                subscription_table.insert(user_id, order_id, platform)

            await ctx.send("訂閱成功！")
        except Exception as e:
            logging.error(f"Error subscribing: {e}")
            await ctx.send("訂閱失敗，請稍後再試！")

    @commands.command("unsubscribe", aliases=["unsub"])
    async def unsubscribe(self, ctx, platform: str, order_id: str):
        user_id = ctx.author.id

        try:
            with Database() as db:
                subscription_table = SubscriptionTable(db)

                # Check if user is in the subscription table
                subscription = subscription_table.get(user_id, order_id, platform)
                print(subscription)
                if not subscription:
                    await ctx.send("沒有訂閱過！")
                    return

                subscription_table.delete(order_id, platform)

            await ctx.send("取消訂閱成功！")
        except Exception:
            await ctx.send("取消訂閱失敗，請稍後再試！")

    @tasks.loop(minutes=30)
    async def check_subscriptions(self):
        with Database() as db:
            subscription_table = SubscriptionTable(db)
            subscriptions = subscription_table.get_all()

            # Generate task arguments
            task_args = []
            for subscription in subscriptions:
                _, user_id, order_id, platform_id, _ = subscription
                _, platform = PlatformTable(db).get(platform_id)
                platform_enum = platform_to_enum[platform]

                task_args.append((platform_enum, order_id))

            # Track parcels concurrently
            with ThreadPoolExecutor() as executor:
                results = executor.map(track, *zip(*task_args))

                for result in results:
                    if result is None:
                        continue

                    # Check if status is different
                    parcel_table = ParcelTable(db)
                    parcel = parcel_table.get(
                        result.order_id, platform_to_id[result.platform]
                    )

                    # If parcel is not found, insert into database
                    if parcel is None:
                        parcel_table.insert(result)
                        order_id = result.order_id
                        status = result.status
                    else:
                        _, order_id, platform_id, status, _ = parcel

                    if status == result.status:
                        continue

                    # Update status
                    parcel_table.update(order_id, platform_id, result.status)

                    # Send message to user
                    file_name = self._get_image_name(result.platform)
                    embed = self._generate_embed(result, file_name)
                    file = File(f"bot/static/img/{file_name}", filename=f"{file_name}")

                    user = await self.bot.fetch_user(user_id)
                    await user.send(embed=embed, file=file)

    # TODO Implement this
    @tasks.loop()
    async def delete_expired_subscriptions(self):
        pass

    def _get_image_name(self, platform: str) -> str:
        match platform:
            case PlatformEnum.SevenEleven.value:
                file_name = "seven.jpg"
            case PlatformEnum.FamilyMart.value:
                file_name = "family.jpg"
            case PlatformEnum.OKMart.value:
                file_name = "ok_mart.png"
            case PlatformEnum.Shopee.value:
                file_name = "shopee.png"
            case _:
                file_name = ""
        return file_name

    def _generate_embed(self, result: TrackingInfo, file_name: str) -> Embed:
        embed = Embed(title="查詢結果", description=f"取貨編號: {result.order_id}")
        embed.set_thumbnail(url=f"attachment://{file_name}")
        embed.add_field(name="包裹狀態", value=result.status)
        if result.time is not None:
            embed.add_field(name="更新時間", value=result.time)
        return embed
