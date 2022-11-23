import steammarket_new as sm


CSGO_ID = 730
TEST_ITEM = 'AK-47 | Redline (Field-Tested)'
TEST_ITEM2 = 'AK-47 | The Empress (Field-Tested)'


def main():
    item_info = sm.get_item_listing(CSGO_ID, TEST_ITEM2)
    print(item_info)


if __name__ == '__main__':
    main()
