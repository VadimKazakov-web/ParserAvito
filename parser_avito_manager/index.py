"""
Шаблон для страницы с результатами
"""


base = """ "<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        * {
            box-sizing: border-box;
            padding: 0;
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
        }
        header {
            padding-top: 20px;
        }
        .container {
            width: 97%;
            margin: 0 auto;
        }
        .main_title {
            margin-bottom: 20px;
        }
        .options {
            margin-bottom: 20px;
        }
        .btn {
            margin-right: 15px;
            margin-bottom: 15px;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
        }
        .btn-focus {
            outline-offset: 2px;
            outline: 2px solid green;
        }
        .result {
            display: none !important;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .elem {
            display: flex;
            flex-direction: column;
            width: 100%;
            border-radius: 5px;
            margin-bottom: 8px;
            background-color: antiquewhite;
            padding: 5px;
        }
        .id {
            color: gray;
        }
        .title {
            font-size: 20px;
        }
        .link {
            display: block;
            width: 100%;
            font-size: 15px;
            word-break: break-all;
        }
        .info {
            padding: 10px 0;
            max-width: 700px;
        }
        .info td {
            padding: 0 3px;
        }
        .display-block-total-views {
            display: block !important;
            .total_views {
                color: green;
                font-weight: bold;
            }
        }
        .display-block-today-views {
            display: block !important;
            .today_views {
                color: green;
                font-weight: bold;
            }
        }
        .display-block-reviews {
            display: block !important;
            .reviews {
                color: green;
                font-weight: bold;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1 class="main_title">
                {title_content}
            </h1>
            <div class="options">
                <button id="btn_total_view" class="btn btn-focus">
                    по просмотрам за всё время
                </button>
                <button id="btn_today_view" class="btn">
                    по просмотрам за сегодня
                </button>
                <button id="btn_review" class="btn">
                    по отзывам
                </button>
            </div>
        </div>
    </header>
    <main>
        <div class="container">
            <div id="block_total_views" class="result display-block-total-views">
                {total_views_content}
            </div>
            <div id="block_today_views" class="result">
                {today_views_content}
            </div>
            <div id="block_review_count" class="result">
                {review_count_content}
            </div>
        </div>
    <script>
        let btn_total_view = document.querySelector('#btn_total_view');
        let btn_today_view = document.querySelector('#btn_today_view');
        let btn_review = document.querySelector('#btn_review');
        let results = document.querySelectorAll('.result');
        let buttons = document.querySelectorAll('.btn');


        let block_total_views = document.querySelector('#block_total_views');
        let block_today_views = document.querySelector('#block_today_views');
        let block_review_count = document.querySelector('#block_review_count');

        function show_result(btn, block, selector) {
            btn.addEventListener("click", () => {
            results.forEach((elem) => {
                elem.classList.remove('display-block-total-views');
                elem.classList.remove('display-block-today-views');
                elem.classList.remove('display-block-reviews');

            })
            buttons.forEach((elem) => {
                elem.classList.remove('btn-focus');
            })
            btn.classList.add('btn-focus');
            block.classList.add(selector);
        })

        }

        show_result(btn_total_view, block_total_views, 'display-block-total-views');
        show_result(btn_today_view, block_today_views, 'display-block-today-views');
        show_result(btn_review, block_review_count, 'display-block-reviews');
    </script>
    </main>
</body>
</html>
"""