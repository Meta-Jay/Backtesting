#include <string>
#include <hdf5.h>

class Database
{
    public:
        Database(const std::string& file_name);
        void close_file();

        hid_t h5_file;
};