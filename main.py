import steam_market.steam_market as sm

TEST_ITEM = 'AK-47 | Redline (Field-Tested)'
TEST_ITEM2 = 'AK-47 | The Empress (Field-Tested)'


def main():
    csgo_items = sm.get_csgo_item_listing(TEST_ITEM2)
    for item in csgo_items.values():
        print(item)
        break


if __name__ == '__main__':
    main()

