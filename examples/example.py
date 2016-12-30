import csv
import logging

from grab.spider import Spider, Task


class ExampleSpider(Spider):
    # List of initial tasks
    # For each URL in this list the Task object will be created
    initial_urls = ('http://habrahabr.ru/', )

    def prepare(self):
        # Prepare the file handler to save results.
        # The method `prepare` is called one time before the
        # spider has started working
        self.result_file = csv.writer(open('result.csv', 'w'))

    def task_initial(self, grab, task):
        print('Habrahabr home page')

        # This handler for the task named `initial i.e.
        # for tasks that have been created from the
        # `self.initial_urls` list

        # As you see, inside handler you can work with Grab
        # in usual way i.e. just if you have done network request
        # manually
        for elem in grab.doc.select('//h2[@class="post__title"]'
                                    '/a[@class="post__title_link"]'):
            # For each title link create new Task
            # with name "habrapost"
            # Pay attention, that we create new tasks
            # with yield call. Also you can use `add_task` method:
            # self.add_task(Task('habrapost', url=...))
            yield Task('habrapost', url=elem.attr('href'))

    def task_habrapost(self, grab, task):
        print('Habrahabr topic: %s' % task.url)

        # This handler receives results of tasks we
        # created for each topic title found on home page

        # First, save URL and title into dictionary
        post = {
            'url': task.url,
            'title': grab.doc.select('//h1[@class="post__title"]'),
        }

        # Next, create new network request to search engine to find
        # the image related to the title.
        # We pass info about the found publication in the arguments to
        # the Task object. That allows us to pass information to next
        # handler that will be called for found image.
        self.result_file.writerow((post['url'], post['title'].text()))
        print(post['url'], post['title'].text())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # Let's start spider with two network concurrent streams
    bot = ExampleSpider(thread_number=2)
    bot.run()
