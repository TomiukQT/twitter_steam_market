import steammarket_new as sm


CSGO_ID = 730
TEST_ITEM = 'AK-47 | Redline (Field-Tested)'
TEST_ITEM2 = 'M4A1-S | Printstream (Field-Tested)'


def main():
    item_info = sm.get_item(CSGO_ID, TEST_ITEM)
    print(item_info)



if __name__ == '__main__':
    main()
