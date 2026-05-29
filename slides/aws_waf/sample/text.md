rule1

```
{
    "Name": "rule1",
    "Priority": 0,
    "Statement": {
        "AndStatement": {
            "Statements": [
                {
                    "GeoMatchStatement": {
                        "CountryCodes": [
                            "JP"
                        ]
                    }
                },
                {
                    "RegexMatchStatement": {
                        "RegexString": ".*/test/.*",
                        "FieldToMatch": {
                            "Body": {
                                "OversizeHandling": "CONTINUE"
                            }
                        },
                        "TextTransformations": [
                            {
                                "Priority": 0,
                                "Type": "URL_DECODE"
                            },
                            {
                                "Priority": 1,
                                "Type": "LOWERCASE"
                            }
                        ]
                    }
                }
            ]
        }
    },
    "VisibilityConfig": {
        "SampledRequestsEnabled": true,
        "CloudWatchMetricsEnabled": true,
        "MetricName": "rule1"
    },
    "Action": {
        "Block": {}
    }
}
```

rul2
```
{
    "Name": "rule2",
    "Priority": 10,
    "Statement": {
        "AndStatement": {
            "Statements": [
                {
                    "GeoMatchStatement": {
                        "CountryCodes": [
                            "US"
                        ]
                    }
                },
                {
                    "RegexMatchStatement": {
                        "RegexString": ".*/example/.*",
                        "FieldToMatch": {
                            "Body": {
                                "OversizeHandling": "CONTINUE"
                            }
                        },
                        "TextTransformations": [
                            {
                                "Priority": 0,
                                "Type": "URL_DECODE"
                            },
                            {
                                "Priority": 1,
                                "Type": "LOWERCASE"
                            }
                        ]
                    }
                }
            ]
        }
    },
    "VisibilityConfig": {
        "SampledRequestsEnabled": true,
        "CloudWatchMetricsEnabled": true,
        "MetricName": "rule2"
    },
    "Action": {
        "Block": {}
    }
}
```