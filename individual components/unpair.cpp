#include <fstream>
using namespace std;
int main(){
  system("echo 'paired-devices' | bluetoothctl > paired.txt");
  ifstream in;
  in.open("paired.txt");
  if (!in.is_open()) return 1;
  string text;
  getline(in, text, (char) in.eof());
  int temp = 0;
  string temp2 = "Device ";
  for (int i = 0; i < text.length(); i++){
    if (text.at(i) == temp2.at(temp)){
      temp++;
    }
    else{
      temp = 0;
    }
    if (temp == 7){
      i++;
      string temp3 = "                 ";
      for (int j = 0; j < 17; j++){
        temp3.at(j) = text.at(i+j);
      }
      system(("echo 'remove " + temp3 + "' | bluetoothctl").c_str());
      i = text.length();
    }
  }
} 
