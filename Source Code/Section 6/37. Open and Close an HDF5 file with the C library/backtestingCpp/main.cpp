#include <iostream>
#include "Database.h"


int main(int, char**) {
    Database db("binance");
    db.close_file();
}