#include <iostream>
#include <cstring>

#include "strategies/Sma.h"


int main(int, char**) {
    std::string symbol = "BTCUSDT";
	std::string exchange = "binance";
	std::string timeframe = "5m";

	char* symbol_char = strcpy((char*)malloc(symbol.length() + 1), symbol.c_str());
	char* exchange_char = strcpy((char*)malloc(exchange.length() + 1), exchange.c_str());
	char* tf_char = strcpy((char*)malloc(timeframe.length() + 1), timeframe.c_str());

    Sma sma(exchange_char, symbol_char, tf_char, 0, 1630074127000);
    sma.execute_backtest(15, 8);
    printf("%f | %f\n", sma.pnl, sma.max_dd);
}