#include <bits/stdc++.h>
using namespace std;

/*
    ソートされた辞書を使う
*/
string sorted_dic_name = "class01/data/sorted_dictionary.txt";

bool length_comp(string a, string b);
map<string, vector<string>> read_sorted_dictionary();

int main () {

    // 辞書読み込み
    map<string, vector<string>> dic = read_sorted_dictionary();
    
    // 入力文字列
    string s;
    cin >> s;
    sort(s.begin(), s.end());

    vector<string> candidates = {""};
    vector<string> anagrams;

    for (char c : s) {
        vector<string> current_candidates = candidates;
        for (string prev : current_candidates) {
            string new_candidate = prev + c;
            if (dic.find(new_candidate) != dic.end()) {
                for (string v : dic[new_candidate]) {
                    anagrams.push_back(v);
                }
            }
            candidates.push_back(new_candidate);
        }
    }

    // 長さsort
    sort(anagrams.begin(), anagrams.end(), length_comp);

    for (string ana : anagrams) {
        cout << ana << endl;
    }
}

// 長さ比較
bool length_comp(string a, string b) {
    return a.size() > b.size();
}

//　ソートされた辞書の読み込み
map<string, vector<string>> read_sorted_dictionary() {
    // key:ソート済文字列, value:ソート前文字列1 ソート前文字列2 ...
    ifstream ifs(sorted_dic_name);
    string str;
    map<string, vector<string>> dic;

    if (ifs.fail()) {
        cerr << "Failed to open file." << endl;
        exit(1);
    }
    while (getline(ifs, str)) {
        stringstream ss;
        ss << str;

        string key, s;
        vector<string> val;
        ss >> key;
        while(getline(ss, s, ' ')) {
            ss >> s;
            val.push_back(s);
        }
         
        dic[key] = val;
    }
    return dic;
}