<?php
header('Content-Type: application/json; charset=utf-8');

$data = [
    "quiz" => [
        [
            "name" => "math",
            "type" => "custom",
            "settings" => [
                "sname" => "xname",
                "question" => "245 + 1 Sorusunun Cevabı Nedir?",
                "options" => [
                    [
                        "name" => "a",
                        "display" => "A)247",
                        "select" => 247
                    ],
                    [
                        "name" => "b",
                        "display" => "B)145",
                        "select" => 145
                    ],
                    [
                        "name" => "c",
                        "display" => "C)246",
                        "select" => 246
                    ]
                ],
                "answer" => "C",
                "answer2" => 246
            ]
            ],
            [
                "name" => "math",
                "type" => "random",
                "settings" => [
                    "sname" => "toplama",
                    "min" => 1,
                    "max" => 100,
                    "operation" => "+"
                ]
            ]
    ]
];


echo json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
