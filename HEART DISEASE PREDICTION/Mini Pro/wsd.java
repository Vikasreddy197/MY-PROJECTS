import java.util.*;
import java.io.*;
import java.lang.*;
class wsd{


public static void phase1(ArrayList<String> test,HashMap<Integer,ArrayList<String>> map,int n,HashMap<String,ArrayList<Double>> result,HashMap<String,Integer> cls,String ambw){
 for(String s:test)
{
 int count=0;
 if(s.equals(ambw))
   count=0;
else
{

 for(Map.Entry<String,Integer> ent:cls.entrySet())
{
  count=0;
  String c=ent.getKey();
  ArrayList<Double> res=new ArrayList<>();
  for(Map.Entry<Integer,ArrayList<String>> entry:map.entrySet())
  {
     if(entry.getValue().get(0).equals(c))
       count+=Collections.frequency(entry.getValue(),s);
  }
System.out.println("word= "+s+"  count= "+count+"  sense: "+c);
  Double ans=Double.valueOf((count+1))/Double.valueOf((ent.getValue()+n));
  res.add(ans);
  if(!result.containsKey(c))
        result.put(c,new ArrayList<Double>(res));
  else
    {  ArrayList<Double> r=result.get(c);
       r.add(ans);
       result.put(c,r);
   }
}
}
}
System.out.println(result);
}

public static void main(String args[])
{
  //Taking training input
int nofunique=0;
  System.out.println("Enter the number of documents in training:");
  Scanner sc=new Scanner(System.in);
  int n=sc.nextInt();
  System.out.println("\nEnter the sense of doc followed by words(eg:1:furniture,put,coat)");
  HashMap<Integer,ArrayList<String>> map=new HashMap<>();
ArrayList<String> totalwords=new ArrayList<String>();
HashMap<String,Integer> cls=new HashMap<>();
  for(int i=0;i<n;i++)
  {
   
   String s=(new Scanner(System.in)).nextLine();
   String[] arr=s.split(":");
   int key=Integer.parseInt(arr[0]);
   String[] words=arr[1].split(",");
 if(!cls.containsKey(words[0]))
    cls.put(words[0],1);
 else
    cls.put(words[0],cls.get(words[0])+1);
  totalwords.addAll(Arrays.asList(words));
  map.put(key,new ArrayList<String>(Arrays.asList(words)));
  }
System.out.println(cls);
HashSet<String> set=new HashSet<String>(totalwords);
//System.out.println(set);



//System.out.println("\n Map contents:"+map.toString()+"  no of unique words:"+(set.size()-2));
  System.out.println("\n Enter the test document:(eg:put,coat,award)");
  String v=(new Scanner(System.in)).nextLine();
  String[] testwords=v.split(",");
  ArrayList<String> test=new ArrayList<String>(Arrays.asList(testwords));
  System.out.println("Enter the ambigous word:");
  String amb=(new Scanner(System.in)).nextLine();
  if(test.contains(amb))
      nofunique=set.size()-3;
  else
      nofunique=set.size()-2;



  HashMap<String,ArrayList<Double>> res=new HashMap<>();

//phase1
phase1(test,map,nofunique,res,cls,amb);

System.out.println("\n Map contents:"+map.toString()+"  no of unique words:"+nofunique);

//phase 2
 for(Map.Entry<String,Integer> entr:cls.entrySet())
  {
        Double ans=Double.valueOf(entr.getValue()+1)/(Double.valueOf(n+nofunique));
       ArrayList<Double> r=res.get(entr.getKey());
       r.add(ans);
       res.put(entr.getKey(),r);
  }
System.out.println(res);
 HashMap<String,Double> fin=new HashMap<>();
 for(Map.Entry<String,ArrayList<Double>> cs:res.entrySet())
{
    Double fans=1.0;
   for(Double db:cs.getValue())
   {
       fans*=db;
   }

  fin.put(cs.getKey(),(Math.log(fans) / Math.log(2)));  
}


System.out.println(fin);
double maxval=Collections.max(fin.values());
for(Map.Entry<String,Double> f:fin.entrySet())
   {
     if(f.getValue()==maxval)
           System.out.println("Sense of doc:"+f.getKey());
   }
}

}