
Учебно-тренировочный проект парсера сайта www.avito.ru написанный на Python,
целью данного проекта было изучение и применение на практике: <br>

* [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/) - для серверной части <br>
* [tkinter](https://docs.python.org/3/library/tkinter.html) - для графического интерфейса. <br>

Данная программа скомпилирована из исходного кода в один exe-файл <br>
с помощью [pyinstaller](https://pypi.org/project/pyinstaller/) и находится в хранилище S3.
<figure>
    <img src="https://s3.twcstorage.ru/parser-avito-download/githab_image/parser_avito_interface.png" width="500" alt="интерфейс программы">
    <figcaption>пользовательский интерфейс программы</figcaption>
</figure>
<br>
<h2>Коротко о дизайне</h2>
Пользовательский интерфейс запускается только в главном потоке программы - это ограничение tkinter.
Серверная часть запускается в отдельном потоке python, <br> 
который в свою очередь порождает ещё один поток-слушатель данных/cобытий из интерфейса.
Собираемая информация из объявлений заносится в базу данных sqllite3.

<h3>Интерфейс</h3>
Окно программы выполнено с использованием стандартной библиотеки tkinter.
Код организован в виде иерархии пакетов, для повышения читаемости, где каждый пакет является фреймом или другим логическим блоком.
<figure>
    <img src="https://s3.twcstorage.ru/parser-avito-download/githab_image/hierarchy_interface.png" width="300" alt="иерархия пакетов">
    <figcaption>иерархия элементов интерфейса</figcaption>
</figure>
<br>
<br>
Действия над виджитами порождают как встроенные, так и пользовательские события tkinter, <br>
которые обрабатываются определёнными методами и функциями. <br>
Например:

    ROOT.event_generate(Events.post_var_event)
    start_btn.event_generate(Events.post_var_event_btn)
    stop_btn.event_generate(Events.post_var_event_btn)
и

    def start(self):
        self.root.bind(Events.push_start_event, func=HandlersClass.valid_all_vars)
        self.root.bind(Events.post_var_event, func=lambda _: connector.put(Variables(HandlersClass.data)))
        self.root.bind(Events.push_stop_event, func=lambda _: connector.put(Events.push_stop_event))
        self.root.bind(Events.create_download_btn_event, func=create_download_prog_btn)
        self.root.mainloop()

Необходимые пользовательские события, <br>
которые выражены в виде констант, а также переменные,
отправляются в очередь queue.Queue, где извлекаются серверной частью.

<h3>Серверная часть</h3>
Из очереди извлекаются необходимые переменные такие как ссылка на целевую категорию,
название результирующего файла, кол-во страниц для сканирования.
После этого запускается работа класса WorkFlow с основной логикой работы:

* открытие/закрытие web страниц, поиск css селектора, осуществляется с помощью **Selenium WebDriver**.<br>
Например поиск css селектора выглядит так:

        block = driver.find_element(by=By.CSS_SELECTOR, value=target_block)
        html = block.get_attribute('innerHTML')

* сбор необходимых данных из объявления осуществляется с помощью регулярных выражений.
* собранная информация из каждого объявления сразу заносится в базу данных.
* после прохождения заданного кол-ва страниц с объявлениями либо наступления другого события остановки, таких как <br>
нажатие кнопки "Stop" или закрытие окна программы, собранные данные извлекаются из базы данных с **заданной сортировкой**, затем записываются в html файл <br>
и отображаются в браузере по умолчанию.

  <figure>
      <img src="https://s3.twcstorage.ru/parser-avito-download/githab_image/result_prog.png" width="700" alt="результат">
      <figcaption>результирующий файл</figcaption>
  </figure>

<h2>Особенности:</h2>
* Поток выполнения главной логики программы в классе WorkFlow, выполнен в виде прохода по "длинному" генератору,
  в месте прерывания генератора добавлены такие методы как проверка определённых событий и актуализация прогресса. <br>
  Например:

      for step in self._work_flow(pages=self._open_pages_global_counter,
                                  advertisement=self._open_advertisement_global_counter):
          # если произошёл обрыв соединения, прекращается текущий проход по генератору,
          # закрывается окно браузера и создаётся новое, генератор перематывается вперёд на
          # нужное кол-во страниц и объявлений
          if step == self._connection_failure:
              break
          # проверка, не произошли ли события нажатия на кнопки stop, exit и т.д...
          EventsConnector.events_handler()
          # актуализация прогресса
          self._update_progress(self.driver)





