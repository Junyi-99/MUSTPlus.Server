## **获取学生 GPA**

  获取最细的 GPA 数据，并且更新 GPA 缓存。如果获取失败，则返回缓存的 GPA 数据。如果连缓存也没有，那么 gpa 字段返回空数组（具体看 Response Example）

  **详细解释：**

  在用户登入 MUST+ 之后，应尽快调用该API，以保证成功获取最新 GPA 数据。

  GPA 数据获取完毕后会被缓存在数据库中，这样，COES Cookie 过期了也不会对服务产生影响，

  如果用户的 COES Cookie 已经过期，那么该 API 会直接返回数据库内缓存的 GPA 数据。

  如果数据库内无缓存的数据，gpa数组字段依然存在，只是数组为空

  所以，通过该 API 调用的数据**不能保证** GPA 为最新。

- **URL**

  _/gpa_

- **Method**

  `GET`

- **REST Params**
  
  None

- **URL Params**

  **Required:**

  `token: string` 登陆时获得的 token

  `time: integer` 10位时间戳 UTC+0

  `sign: string` 当前请求的签名

- **Data Params**

  None

- **调用成功返回样例 Response Example**

如果数据库中有用户成绩缓存：

```JSON
{
    "code": 0,
    "msg": "",
    "gpa": [
        {
            "course_intake": 1709,
            "total_credit": 23.0,
            "pass_credit": 23.0,
            "fail_credit": 0.0,
            "gpa_credit": 23.0,
            "gpa": 3.71,
            "accum_gpa": 3.71,
            "details": [
                {
                    "course_code": "CN103",
                    "course_name_zh": "計算機程序設計 I",
                    "credit": "4.0",
                    "grade": "A+",
                    "exam_datetime": null,
                    "exam_classroom": "C304",
                    "exam_seat": "1045"
                },
                {
                    "course_code": "GSER111",
                    "course_name_zh": "大學英語 (精讀 I)",
                    "credit": "6.0",
                    "grade": "B",
                    "exam_datetime": null,
                    "exam_classroom": "C308",
                    "exam_seat": "1226"
                }
            ]
        },
        {
            "course_intake": 1802,
            "total_credit": 30.0,
            "pass_credit": 30.0,
            "fail_credit": 0.0,
            "gpa_credit": 30.0,
            "gpa": 3.9,
            "accum_gpa": 3.82,
            "details": [
                {
                    "course_code": "CHN301",
                    "course_name_zh": "大學語文",
                    "credit": "3.0",
                    "grade": "A-",
                    "exam_datetime": null,
                    "exam_classroom": "N418",
                    "exam_seat": "2280"
                }
            ]
        },
        {
            "course_intake": 1809,
            "total_credit": 14.0,
            "pass_credit": 14.0,
            "fail_credit": 0.0,
            "gpa_credit": 14.0,
            "gpa": 3.96,
            "accum_gpa": 3.85,
            "details": [
                {
                    "course_code": "GLL026-30",
                    "course_name_zh": "語言文字專題項目 (一) 之「葡語入門」",
                    "credit": "2.0",
                    "grade": "A+",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                },
                {
                    "course_code": "LP002",
                    "course_name_zh": "數據結構",
                    "credit": "4.0",
                    "grade": "A+",
                    "exam_datetime": null,
                    "exam_classroom": "C302",
                    "exam_seat": "856"
                },
                {
                    "course_code": "MA109",
                    "course_name_zh": "線性代數與概率統計",
                    "credit": "4.0",
                    "grade": "A",
                    "exam_datetime": null,
                    "exam_classroom": "B202a",
                    "exam_seat": "176"
                },
                {
                    "course_code": "PEC101",
                    "course_name_zh": "少林養身功",
                    "credit": "1.0",
                    "grade": "A+",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                },
                {
                    "course_code": "PET101",
                    "course_name_zh": "太極拳",
                    "credit": "1.0",
                    "grade": "A+",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                }
            ]
        },
        {
            "course_intake": 1902,
            "total_credit": 17.0,
            "pass_credit": 17.0,
            "fail_credit": 0.0,
            "gpa_credit": 17.0,
            "gpa": 3.93,
            "accum_gpa": 3.86,
            "details": [
                {
                    "course_code": "CE107",
                    "course_name_zh": "數字電路基礎",
                    "credit": "4.0",
                    "grade": "A-",
                    "exam_datetime": null,
                    "exam_classroom": "C302",
                    "exam_seat": "792"
                },
                {
                    "course_code": "CN105",
                    "course_name_zh": "Web技術概論",
                    "credit": "3.0",
                    "grade": "A",
                    "exam_datetime": null,
                    "exam_classroom": "C307",
                    "exam_seat": "946"
                },
                {
                    "course_code": "CS101",
                    "course_name_zh": "數據庫系統",
                    "credit": "4.0",
                    "grade": "A",
                    "exam_datetime": null,
                    "exam_classroom": "C308",
                    "exam_seat": "1006"
                },
                {
                    "course_code": "LP104",
                    "course_name_zh": "面向對象程序設計",
                    "credit": "6.0",
                    "grade": "A+",
                    "exam_datetime": null,
                    "exam_classroom": "C307",
                    "exam_seat": "944"
                }
            ]
        },
        {
            "course_intake": 1909,
            "total_credit": 18.0,
            "pass_credit": 18.0,
            "fail_credit": 0.0,
            "gpa_credit": 18.0,
            "gpa": 4.0,
            "accum_gpa": 3.89,
            "details": [
                {
                    "course_code": "CO101",
                    "course_name_zh": "計算機組成原理",
                    "credit": "5.0",
                    "grade": "A+",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                },
                {
                    "course_code": "CS104",
                    "course_name_zh": "計算機圖形學基礎",
                    "credit": "3.0",
                    "grade": "A+",
                    "exam_datetime": null,
                    "exam_classroom": "C308",
                    "exam_seat": "993"
                },
                {
                    "course_code": "CS106",
                    "course_name_zh": "編譯原理",
                    "credit": "3.0",
                    "grade": "A+",
                    "exam_datetime": null,
                    "exam_classroom": "C302",
                    "exam_seat": "787"
                },
                {
                    "course_code": "CS108",
                    "course_name_zh": "數據庫系統進階",
                    "credit": "4.0",
                    "grade": "A+",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                },
                {
                    "course_code": "ME102",
                    "course_name_zh": "電子商務",
                    "credit": "3.0",
                    "grade": "A+",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                }
            ]
        },
        {
            "course_intake": 2002,
            "total_credit": 23.0,
            "pass_credit": 0.0,
            "fail_credit": 0.0,
            "gpa_credit": 0.0,
            "gpa": 0.0,
            "accum_gpa": 3.89,
            "details": [
                {
                    "course_code": "CN007",
                    "course_name_zh": "數據安全",
                    "credit": "3.0",
                    "grade": "",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                },
                {
                    "course_code": "CN101",
                    "course_name_zh": "計算機網絡",
                    "credit": "5.0",
                    "grade": "",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                },
                {
                    "course_code": "CO003",
                    "course_name_zh": "操作系統",
                    "credit": "5.0",
                    "grade": "",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                },
                {
                    "course_code": "CO004",
                    "course_name_zh": "操作系統實踐",
                    "credit": "4.0",
                    "grade": "",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                },
                {
                    "course_code": "CS105",
                    "course_name_zh": "人工智能基礎",
                    "credit": "3.0",
                    "grade": "",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                },
                {
                    "course_code": "ST001",
                    "course_name_zh": "計算機新技術專題",
                    "credit": "3.0",
                    "grade": "",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                }
            ]
        },
        {
            "course_intake": 2009,
            "total_credit": 17.0,
            "pass_credit": 0.0,
            "fail_credit": 0.0,
            "gpa_credit": 0.0,
            "gpa": 0.0,
            "accum_gpa": 3.89,
            "details": [
                {
                    "course_code": "CN102",
                    "course_name_zh": "計算機網絡應用技術",
                    "credit": "2.0",
                    "grade": "",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                },
                {
                    "course_code": "CN108",
                    "course_name_zh": "計算機網絡應用技術實踐",
                    "credit": "3.0",
                    "grade": "",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                },
                {
                    "course_code": "CS003",
                    "course_name_zh": "軟件工程實踐",
                    "credit": "4.0",
                    "grade": "",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                },
                {
                    "course_code": "CS014",
                    "course_name_zh": "軟件工程",
                    "credit": "4.0",
                    "grade": "",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                },
                {
                    "course_code": "CN106",
                    "course_name_zh": "網絡程序設計",
                    "credit": "4.0",
                    "grade": "",
                    "exam_datetime": null,
                    "exam_classroom": "",
                    "exam_seat": ""
                }
            ]
        }
    ]
}
```

如果没有成绩缓存，并且 COES Cookie失效：

```json
{
  "code": 0,
  "msg": "",
  "gpa": []
}
```


- **Error Response:**

    会遇到 AUTH 系列的错误（用户未登录或未经授权的访问）

    `AUTH_UNKNOWN_ERROR = -1000  # 未知错误`
    
    `AUTH_SIGN_VERIFICATION_FAILED = -1001  # sign 验证失败`
    
    `AUTH_TIME_INVALID = -1002  # 请求已过期`
    
    `AUTH_TOKEN_INVALID = -1003  # token 无效`
    
    `AUTH_REQUEST_METHOD_ERROR = -1004  # 请求方法错误`
    
    `AUTH_VALIDATE_ARGUMENT_ERROR = -1005  # 校验参数错误`
  
    还会遇到
    
    `OK = 0  # 正常`
    
    `WARNING = 1  # 警告（一般可忽略）`
    
    `INTERNAL_ERROR = 2  # 内部错误`
    
    `PAGE_NOT_FOUND = 3  # 页面未找到 （404）`
    
    `MISSING_FIELD = 4  # 缺少字段`
    
    `INVALID_PARAM = 5`