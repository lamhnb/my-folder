// Exact six-ticket Power 6/55 portfolio distribution (research-only).
// Compile: g++ -std=c++17 -O3 power655_portfolio_exact_20261103.cpp -o exact && ./exact
#include <array>
#include <vector>
#include <string>
#include <iostream>
#include <cstdint>
#include <algorithm>
using namespace std;
using Ticket = array<int,6>;
using Portfolio = array<Ticket,6>;
int main(){
 Portfolio A={{{2,4,7,19,21,26},{11,24,27,49,52,55},{5,18,28,36,41,47},{8,15,23,25,38,40},{1,6,13,14,34,51},{9,17,20,31,45,50}}};
 Portfolio B=A,C=A,D=A;
 B[1][0]=A[0][0];B[3][0]=A[2][0];B[5][0]=A[4][0];
 for(int k=0;k<2;k++){C[1][k]=A[0][k];C[3][k]=A[2][k];C[5][k]=A[4][k];}
 for(int j=1;j<6;j++)for(int k=0;k<3;k++)D[j][k]=A[0][k];
 vector<pair<string,Portfolio>> inputs={{"disjoint36",A},{"overlap1",B},{"overlap2",C},{"common_core3",D}};
 for(auto const& item:inputs){
   auto const& name=item.first; auto const& p=item.second;
   array<uint64_t,6> masks={};uint64_t unique=0;
   for(int j=0;j<6;j++){for(int n:p[j]){if(n<1||n>55){cerr<<"invalid number";return 1;}masks[j]|=1ULL<<(n-1);}if(__builtin_popcountll(masks[j])!=6){cerr<<"duplicate in ticket";return 1;}unique|=masks[j];for(int k=0;k<j;k++)if(masks[j]==masks[k]){cerr<<"duplicate ticket";return 1;}}
   array<uint64_t,7> best={};uint64_t any3=0,any4=0,any5=0,any6=0,multi3=0,multi4=0,multi5=0,sum3=0,sum4=0,sum5=0,sum6=0,total=0;
   for(int a=0;a<50;a++)for(int b=a+1;b<51;b++)for(int c=b+1;c<52;c++)for(int d=c+1;d<53;d++)for(int e=d+1;e<54;e++)for(int f=e+1;f<55;f++){
     uint64_t draw=(1ULL<<a)|(1ULL<<b)|(1ULL<<c)|(1ULL<<d)|(1ULL<<e)|(1ULL<<f);
     int mx=0,n3=0,n4=0,n5=0,n6=0;
     for(auto mask:masks){int h=__builtin_popcountll(mask&draw);mx=max(mx,h);n3+=(h>=3);n4+=(h>=4);n5+=(h>=5);n6+=(h>=6);}
     best[mx]++;any3+=(n3>0);any4+=(n4>0);any5+=(n5>0);any6+=(n6>0);
     multi3+=(n3>=2);multi4+=(n4>=2);multi5+=(n5>=2);
     sum3+=n3;sum4+=n4;sum5+=n5;sum6+=n6;total++;
   }
   if(total!=28989675ULL){cerr<<"incorrect enumeration";return 1;}
   cout<<name<<" unique="<<__builtin_popcountll(unique)<<" total="<<total;
   for(int k=0;k<=6;k++)cout<<" best"<<k<<"="<<best[k];
   cout<<" any3="<<any3<<" any4="<<any4<<" any5="<<any5<<" any6="<<any6;
   cout<<" multi3="<<multi3<<" multi4="<<multi4<<" multi5="<<multi5;
   cout<<" sum3="<<sum3<<" sum4="<<sum4<<" sum5="<<sum5<<" sum6="<<sum6<<"\n";
 }
}
