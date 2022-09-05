MAP_URL_API_WEB = [
    ('/api/news/detail', '/news/detail/'),
    ('/api/hotels/detail-hotel/.*', '/hotel/detail/?/'),
    ('/api/car/.*', '/book-car/detail/?'),
    ('/api/ticket_visit/detail-ticket-visit/.*', '/visit-ticket/detail/?/'),
    ('/api/tourguide/.*/detail', '/tour-guide/?/'),
    ('/api/special/.*/detail', '/product/detail/?/'),

]
SCHEMA_HOST_WEB = 'http://10.10.10.94:7000'