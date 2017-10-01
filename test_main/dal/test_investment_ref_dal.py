# encoding: UTF-8
import main
from dal import investment_ref_dal as irdal


def test_get_restricted_stock():
    df = irdal.get_restricted_stock()
    assert df
    df = irdal.get_restricted_stock(2050)
    assert not df


def test_delete_restricted_stock():
    assert irdal.delete_restricted_stock(2017, 10)


if __name__ == '__main__':
    main.setup_logging()
    test_delete_restricted_stock()


