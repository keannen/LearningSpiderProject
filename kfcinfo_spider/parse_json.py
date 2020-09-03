kfc_json = {
	"Table": [{
		"rowcount": 440
	}],
	"Table1": [{
		"rownum": 1,
		"storeName": "前门",
		"addressDetail": "西城区前门西大街正阳市场1号楼中部",
		"pro": "Wi-Fi,礼品卡",
		"provinceName": "北京市",
		"cityName": "北京市"
	}, {
		"rownum": 2,
		"storeName": "京源",
		"addressDetail": "左家庄新源街24号",
		"pro": "Wi-Fi,礼品卡,生日餐会",
		"provinceName": "北京市",
		"cityName": "北京市"
	}, {
		"rownum": 3,
		"storeName": "东大桥",
		"addressDetail": "朝外大街东大桥路1号楼",
		"pro": "Wi-Fi,店内参观,礼品卡",
		"provinceName": "北京市",
		"cityName": "北京市"
	}, {
		"rownum": 4,
		"storeName": "方庄",
		"addressDetail": "蒲芳路26号",
		"pro": "Wi-Fi,店内参观,礼品卡,生日餐会",
		"provinceName": "北京市",
		"cityName": "北京市"
	}, {
		"rownum": 5,
		"storeName": "安定门",
		"addressDetail": "安定门外大街西河沿13号楼",
		"pro": "Wi-Fi,礼品卡,生日餐会",
		"provinceName": "北京市",
		"cityName": "北京市"
	}, {
		"rownum": 6,
		"storeName": "航天桥",
		"addressDetail": "阜成路51-2",
		"pro": "24小时,店内参观",
		"provinceName": "北京市",
		"cityName": "北京市"
	}, {
		"rownum": 7,
		"storeName": "展览路(德宝)",
		"addressDetail": "西外大街德宝新园14号",
		"pro": "Wi-Fi,店内参观,礼品卡",
		"provinceName": "北京市",
		"cityName": "北京市"
	}, {
		"rownum": 8,
		"storeName": "劲松",
		"addressDetail": "劲松4区401楼",
		"pro": "24小时,Wi-Fi,店内参观,礼品卡,生日餐会",
		"provinceName": "北京市",
		"cityName": "北京市"
	}, {
		"rownum": 9,
		"storeName": "西罗园",
		"addressDetail": "西罗园4区南二段",
		"pro": "Wi-Fi,店内参观,礼品卡,生日餐会",
		"provinceName": "北京市",
		"cityName": "北京市"
	}, {
		"rownum": 10,
		"storeName": "蓝桥",
		"addressDetail": "蓝桥餐厅工体北路11－1号",
		"pro": "24小时,Wi-Fi,点唱机,礼品卡",
		"provinceName": "北京市",
		"cityName": "北京市"
	}]
}

info = kfc_json['Table1']
all_info = []
for shop in info:
    item = {}
    item['store_name'] = shop['storeName']
    item['address'] = shop['addressDetail']
    item['city'] = shop['provinceName']
    all_info.append(item)
print(all_info)
