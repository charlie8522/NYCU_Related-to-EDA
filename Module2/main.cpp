#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
vector<vector<string> > crossBoundary;
vector<string> Vout;
int Flag = 0;

class Quad
{
    Quad *LR;
    Quad *LL;
    Quad *UR;
    Quad *UL;
  public:
      vector<vector<string> > data;
      Quad()
      {
          LR = NULL;
          LL = NULL;
          UR = NULL;
          UL = NULL;
      }
};

int checkStatus(float r_Minx,float r_Miny,float r_Maxx,float r_Maxy,float p_Minx,float p_Miny,float p_Maxx,float p_Maxy,auto polygon)
{

    float xhalf = (r_Maxx-r_Minx)/2;
    float yhalf = (r_Maxy-r_Miny)/2;
    //out of boundary
    if((p_Maxx < r_Minx) || (p_Minx > r_Maxx) || (p_Maxy < r_Miny) || (p_Miny > r_Maxy))
    {return 0;}
    //cross boundary
    else if((p_Minx <= r_Minx && p_Maxx >= r_Minx) || (p_Minx <= r_Maxx && p_Maxx >= r_Maxx) || (p_Miny <= r_Miny && p_Maxy >= r_Miny) || (p_Miny <= r_Maxy && p_Maxy >= r_Maxy))
    {
        Vout.push_back(polygon);
        return 1;
    }
    //UL
    else if(p_Minx > r_Minx && p_Maxx < xhalf && p_Maxy < p_Maxy && p_Miny > yhalf)
    {
        Flag = checkStatus(r_Minx,yhalf,xhalf,r_Maxy,p_Minx,p_Miny,p_Maxx,p_Maxy,polygon);
        return 2;
    }
    //UR
    else if(p_Minx > xhalf && p_Maxx < p_Maxx && p_Maxy < p_Maxy && p_Miny > yhalf)
    {
        Flag = checkStatus(xhalf,yhalf,r_Maxx,r_Maxy,p_Minx,p_Miny,p_Maxx,p_Maxy,polygon);
        return 3;
    }
    //LL
    else if(p_Minx > r_Minx && p_Maxx < xhalf && p_Maxy < xhalf && p_Miny > p_Miny)
    {
        Flag = checkStatus(r_Minx,r_Miny,xhalf,yhalf,p_Minx,p_Miny,p_Maxx,p_Maxy,polygon);
        return 4;
    }
    //LR
    else if(p_Minx > xhalf && p_Maxx < p_Maxx && p_Maxy < xhalf && p_Miny > p_Miny)
    {
        Flag = checkStatus(xhalf,r_Miny,r_Maxx,yhalf,p_Minx,p_Miny,p_Maxx,p_Maxy,polygon);
        return 5;
    }
    //intersect half lines
    else
    {
        Vout.push_back(polygon);
        return 6;
    }
}

int main(int argc, char *argv[])
{
    ifstream infile1;
    ifstream infile2;
    ofstream outfile;
    vector <vector<string>> Polygon,Region;

    infile1.open(argv[1]);
    infile2.open(argv[2]);
    outfile.open(argv[3]);

    if(infile1.is_open())
    {
        string line1;
        string polygon,xmin,ymin,xmax,ymax;
        while(getline(infile1,line1))
        {
            stringstream ss(line1);
            getline(ss,polygon,' ');
            getline(ss,xmin,' ');
            getline(ss,ymin,' ');
            getline(ss,xmax,' ');
            getline(ss,ymax,';');
            vector<string> v1 = {polygon,xmin,ymin,xmax,ymax};
            Polygon.push_back(v1);
        }
    }
    if(infile2.is_open())
    {
        string line2;
        string region,Xmin,Ymin,Xmax,Ymax;
        while(getline(infile2,line2))
        {
            stringstream ss(line2);
            getline(ss,region,' ');
            getline(ss,Xmin,' ');
            getline(ss,Ymin,' ');
            getline(ss,Xmax,' ');
            getline(ss,Ymax,';');
            vector<string> v2 = {region,Xmin,Ymin,Xmax,Ymax};
            //cout << region << endl;
            Region.push_back(v2);
        }
    }
    infile1.close();
    infile2.close();
    for(int i=0;i<Region.size();i++)
    {
        int cnt = 0;
        auto region = Region[i][0];
        float r_minx = stof(Region[i][1]);
        float r_maxx = stof(Region[i][2]);
        float r_miny = stof(Region[i][3]);
        float r_maxy = stof(Region[i][4]);
        Vout.push_back(Region[i][0]);
        for (int j=0;j<Polygon.size();j++)
        {
            //cout << Polygon[j][0]<<endl;
            auto polygon = Polygon[j][0];
            float p_minx = stof(Polygon[j][1]);
            float p_maxx = stof(Polygon[j][2]);
            float p_miny = stof(Polygon[j][3]);
            float p_maxy = stof(Polygon[j][4]);
            vector<string> v3 = {Polygon[j][0],Polygon[j][1],Polygon[j][2],Polygon[j][3],Polygon[j][4]};
            Quad a;
            int flag = checkStatus(r_minx,r_miny,r_maxx,r_maxy,p_minx,p_miny,p_maxx,p_maxy,polygon);
            if(flag == 6)
            {
                a.data.push_back(v3);
            }
            else
            {}
        }

        int s = Vout.size();
        if(s != 1)
        {
            for(int k=0;k<s-1;k++)
            {
                outfile << Vout[k] << ' ';
            }
            outfile << Vout[s-1]<<';'<<endl;
        }
        Vout.clear();

    }
    return 0;
}
