#include "Sma.h"
#include "../Database.h"
#include "../Utils.h"


using namespace std;


Sma::Sma(char* exchange_c, char* symbol_c, char* timeframe_c, long long from_time, long long to_time)
{
    exchange = exchange_c;
    symbol = symbol_c;
    timeframe = timeframe_c;

    Database db(exchange);
    int array_size = 0;
    double** res = db.get_data(symbol, exchange, array_size);
    db.close_file();

    std::tie(ts, open, high, low, close, volume) = rearrange_candles(res, timeframe, from_time, to_time, array_size);
}

void Sma::execute_backtest(int slow_ma, int fast_ma)
{

}