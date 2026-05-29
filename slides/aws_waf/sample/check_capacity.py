"""
slides/aws_waf/sample/text.md の rule1 / rule2 を check_capacity API に投げ、
- ルール単体の WCU
- 2 ルールを束ねた場合の実消費 WCU
を比較するスクリプト。

Usage:
    AWS_REGION=ap-northeast-1 python check_capacity.py
"""

import boto3

RULE1 = {
    "Name": "rule1",
    "Priority": 0,
    "Statement": {
        "AndStatement": {
            "Statements": [
                {"GeoMatchStatement": {"CountryCodes": ["JP"]}},
                {
                    "RegexMatchStatement": {
                        "RegexString": ".*/test/.*",
                        "FieldToMatch": {"Body": {"OversizeHandling": "CONTINUE"}},
                        "TextTransformations": [
                            {"Priority": 0, "Type": "URL_DECODE"},
                            {"Priority": 1, "Type": "LOWERCASE"},
                        ],
                    }
                },
            ]
        }
    },
    "VisibilityConfig": {
        "SampledRequestsEnabled": True,
        "CloudWatchMetricsEnabled": True,
        "MetricName": "rule1",
    },
    "Action": {"Block": {}},
}

RULE2 = {
    "Name": "rule2",
    "Priority": 10,
    "Statement": {
        "AndStatement": {
            "Statements": [
                {"GeoMatchStatement": {"CountryCodes": ["US"]}},
                {
                    "RegexMatchStatement": {
                        "RegexString": ".*/example/.*",
                        "FieldToMatch": {"Body": {"OversizeHandling": "CONTINUE"}},
                        "TextTransformations": [
                            {"Priority": 0, "Type": "URL_DECODE"},
                            {"Priority": 1, "Type": "LOWERCASE"},
                        ],
                    }
                },
            ]
        }
    },
    "VisibilityConfig": {
        "SampledRequestsEnabled": True,
        "CloudWatchMetricsEnabled": True,
        "MetricName": "rule2",
    },
    "Action": {"Block": {}},
}


def main():
    client = boto3.client("wafv2")

    only1 = client.check_capacity(Scope="REGIONAL", Rules=[RULE1])["Capacity"]
    only2 = client.check_capacity(Scope="REGIONAL", Rules=[RULE2])["Capacity"]
    both = client.check_capacity(Scope="REGIONAL", Rules=[RULE1, RULE2])["Capacity"]

    print("=" * 40)
    print(f"rule1 単体        : {only1} WCU")
    print(f"rule2 単体        : {only2} WCU")
    print(f"単純合計          : {only1 + only2} WCU")
    print(f"check_capacity 実測 : {both} WCU")
    print(f"最適化による削減  : {only1 + only2 - both} WCU")
    print("=" * 40)


if __name__ == "__main__":
    main()
