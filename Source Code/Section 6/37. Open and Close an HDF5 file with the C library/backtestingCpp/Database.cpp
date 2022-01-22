#include "Database.h"

using namespace std;

Database::Database(const string& file_name)
{
    string FILE_NAME = "../../data/" + file_name + ".h5";
    hid_t fapl = H5Pcreate(H5P_FILE_ACCESS);

    herr_t status = H5Pset_libver_bounds(fapl, H5F_LIBVER_LATEST, H5F_LIBVER_LATEST);
    status = H5Pset_fclose_degree(fapl, H5F_CLOSE_STRONG);

    printf("Opening %s\n", FILE_NAME.c_str());
    h5_file = H5Fopen(FILE_NAME.c_str(), H5F_ACC_RDONLY, fapl);

    if (h5_file < 0) {
        printf("Error while opening %s\n", FILE_NAME.c_str());
    }
}

void Database::close_file()
{
    H5Fclose(h5_file);
}