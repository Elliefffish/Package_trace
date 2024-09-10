from parcel_tw import Platform

platform_to_id = {"seven_eleven": 1, "family_mart": 2, "ok_mart": 3, "shopee": 4}

platform_to_enum = {
    "小七": Platform.SevenEleven,
    "7-11": Platform.SevenEleven,
    "seven": Platform.SevenEleven,
    "seven-eleven": Platform.SevenEleven,
    "seven_eleven": Platform.SevenEleven,
    "711": Platform.SevenEleven,
    "全家": Platform.FamilyMart,
    "family": Platform.FamilyMart,
    "family-mart": Platform.FamilyMart,
    "family_mart": Platform.FamilyMart,
    "fami": Platform.FamilyMart,
    "ok": Platform.OKMart,
    "okmart": Platform.OKMart,
    "ok-mart": Platform.OKMart,
    "ok_mart": Platform.OKMart,
    "蝦皮": Platform.Shopee,
    "shopee": Platform.Shopee,
}
