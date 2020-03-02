#include <iostream>
#include <string>
#include <cstring>


using namespace std;


int main() {
    cout << "Enter password:" << endl;

    string secret;
    cin >> secret;

    char pass[secret.size() + 1];
    strcpy(pass, secret.c_str());
    if (secret.size() != 32) {
        cout << "Nope." << endl;
        return 0;
    }
    //generate_malloc();
    for (int i = 0; i < 8; i++) {
        char t = pass[i * 2];
        pass[i * 2] = pass[i * 2 + 1];
        pass[i * 2 + 1] = t;
    }
    string password;
    for (int i = 0; i < 16; i++)
        password += pass[i];
    if (password.compare("lfgar{g1thP_54}5") == 0) {
        cout << "You are true hacker!" << endl;
        cout << "flag is: " << secret.substr(0, 16) << endl;
    } else { cout << "Nooooope."; }
}

