import wikipedia


def get_info(suburb):
    # wikipedia.page('Kingsford, New South Wales')
    place_name = suburb+', New South Wales'
    p = wikipedia.page(place_name)

    return p.content

print(get_info('Kingsford'))