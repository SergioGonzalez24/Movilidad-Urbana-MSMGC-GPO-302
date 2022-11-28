// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2021

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class Agents
{
    public List<Vector3> positions;
    public List<int> objType;
}

public class Semaforos
{
    public List<Vector3> positions;
    public List<bool> states;
}

public class RunHandler
{
    public string message;
}
public class AgentController : MonoBehaviour
{
    [SerializeField] string url;
    [SerializeField] string configEP;
    [SerializeField] string updateEP;
    [SerializeField] string carEP;
    [SerializeField] string trafficEP;
    [SerializeField] int numAgents;
    [SerializeField] GameObject carPrefab;
    [SerializeField] GameObject semPrefab;
    [SerializeField] float updateDelay;
    Agents agents;
    Semaforos semaforos;
    GameObject[] cars;
    GameObject[] semaforoList;

    public float updateTime = 0;
    bool isFinished = false;
    int finishCounter = 30;
    List<Vector3> oldPositions;
    List<Vector3> newPositions;
    public float dt;
    bool hold = false;
    // Start is called before the first frame update
    void Start()
    {
        oldPositions = new List<Vector3>();
        newPositions = new List<Vector3>();
        cars = new GameObject[numAgents];
        semaforoList = new GameObject[24];
        for (int i = 0; i < numAgents; i++){
            cars[i] = Instantiate(carPrefab, Vector3.zero, Quaternion.identity);
        }
        for (int i = 0; i < 24; i++){
            semaforoList[i] = Instantiate(semPrefab, Vector3.zero, Quaternion.identity);
        }
        StartCoroutine(SendConfiguration());
    }

    // Update is called once per frame
    void Update()
    {   
        float t = updateTime/updateDelay;
        dt = t * t * (3f - 2f*t);
            if(!isFinished || finishCounter > 0){
                if(updateTime > updateDelay){
                    hold = true;
                    StartCoroutine(UpdatePositions());
                    updateTime = 0;
                }
                updateTime += Time.deltaTime;
            }
            if (!hold)
        {
            
            for (int s = 0; s < cars.Length; s++)
            {
                Vector3 interpolated = Vector3.Lerp(oldPositions[s], newPositions[s], dt);
                cars[s].transform.localPosition = interpolated;
                
                Vector3 dir = oldPositions[s] - newPositions[s];
                cars[s].transform.rotation = Quaternion.LookRotation(dir);
                
            }
            if(isFinished){finishCounter -= 1;}
            
    }
    
    }


    IEnumerator UpdatePositions()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + updateEP);
        yield return www.SendWebRequest();

        if(www.result == UnityWebRequest.Result.Success){
            //Debug.Log(www.downloadHandler.text);
            RunHandler handler = JsonUtility.FromJson<RunHandler>(www.downloadHandler.text);
            if(handler.message == "Finished"){
                isFinished = true;
            }
            StartCoroutine(UpdateCarPositions());
            StartCoroutine(UpdateTrafficLights());
        } else {
            Debug.Log(www.error);
        }

    }
    IEnumerator UpdateCarPositions()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + carEP);
        yield return www.SendWebRequest();

        if(www.result == UnityWebRequest.Result.Success){
            //Debug.Log(www.downloadHandler.text);
            agents = JsonUtility.FromJson<Agents>(www.downloadHandler.text);

            // Store the old positions for each agent
            oldPositions = new List<Vector3>(newPositions);

            newPositions.Clear();

            foreach(Vector3 v in agents.positions)
                newPositions.Add(v);

            hold = false;
        } else {
            Debug.Log(www.error);
        }
    }

    IEnumerator UpdateTrafficLights()
    {
        UnityWebRequest www = UnityWebRequest.Get(url + trafficEP);
        yield return www.SendWebRequest();

        if(www.result == UnityWebRequest.Result.Success){
            //Debug.Log(www.downloadHandler.text);
            semaforos = JsonUtility.FromJson<Semaforos>(www.downloadHandler.text);
            MoveSem();
            
        } else {
            Debug.Log(www.error);
        }
    }

    
    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();
        form.AddField("numAgents", numAgents.ToString());
        UnityWebRequest www = UnityWebRequest.Post(url + configEP, form);
        yield return www.SendWebRequest();

        if(www.result == UnityWebRequest.Result.Success){
            Debug.Log(www.downloadHandler.text);
        } else {
            Debug.Log(www.error);
        }
    }

    void MoveSem()
    {
        for (int i=0; i<24; i++) {
            semaforoList[i].transform.position = semaforos.positions[i];
            semaforoList[i].GetComponent<SemaforoLuz>().toggleLight(semaforos.states[i]);
            Debug.Log(semaforos.states[i]);
        }
        
    }
}
