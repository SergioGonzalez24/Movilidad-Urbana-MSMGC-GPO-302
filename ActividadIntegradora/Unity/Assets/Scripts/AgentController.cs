    // TC2008B. Sistemas Multiagentes y Gr�ficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
/*# ----------------------------------------------------------
# Actividad Integradora AgentController.cs
#
# Date: 21-Nov-2022
# Authors:
#           Sergio Manuel Gonzalez Vargas - A01745446
#           Gilberto André García Gaytán - A01753176
#           Fernando Ortiz Saldaña - A01376737
#           Ricardo Ramírez Condado - A01379299
# ----------------------------------------------------------*/

/* Importing the libraries that are going to be used in the code. */
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

/* It's a class that holds the data of a robot */
[Serializable]/* It's a class that holds the data of a robot */

public class RobotData
{
    public string id;
    public float x, y, z;
    public bool hasBox;

    public RobotData(string id, float x, float y, float z, bool hasBox)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.hasBox = hasBox;
    }
}

[Serializable]
/* It's a list of RobotData objects */
public class DatosAgentes
{
    public List<RobotData> positions;

    public DatosAgentes() => this.positions = new List<RobotData>();
}


[Serializable]
/* It's a class that contains the data of a box */
public class DatosCajas
{
    public string id;
    public float x, y, z;
    public bool picked_up;

    public DatosCajas(string id, float x, float y, float z, bool picked_up)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.picked_up = picked_up;
    }
}

[Serializable]
/* It's a list of DatosCajas objects */
public class DatosCaja
{
    public List<DatosCajas> positions;

    public DatosCaja() => this.positions = new List<DatosCajas>();
}

[Serializable]
/* A class that contains the data of the pallets. */
public class DatosTarimas
{
    public string id;
    public float x, y, z;
    public int value;
/* It's a constructor for the DatosTarimas class. */
    public DatosTarimas(string id, float x, float y, float z, int value)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
        this.value = value;
    }
}

[Serializable]
/* It's a list of DatosTarimas objects */
public class Tarimas
{
    public List<DatosTarimas> positions;

    public Tarimas() => this.positions = new List<DatosTarimas>();
}

/* It's a controller for the agents. */
public class AgentController : MonoBehaviour
{
    // private string url = "https://agents.us-south.cf.appdomain.cloud/";
    string serverUrl = "http://localhost:8585";
    string getCajasEndpoint = "/getCajas";
    string getAgentsEndpoint = "/getAgentes";
    string getTarimasEndpoint = "/getTarimas";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    DatosAgentes robotsData;
    DatosCaja boxesData;
    Tarimas palletsData;
    Dictionary<string, GameObject> boxes;
    Dictionary<string, GameObject> robots;
    Dictionary<string, GameObject> pallets;
    Dictionary<string, Vector3> prevPositions, currPositions;

    bool updated = false, started = false;
    bool startedBox = false, startedPallet = false;

    public GameObject pallet, robot, caja, floor;
    public int NBoxes, width, height;
    public float timeToUpdate;
    private float timer, dt;

    // Start is called before the first frame update
/// It initializes the data structures that will be used to store the information about the robots,
/// boxes and pallets, and it also initializes the floor
    void Start()
    {
        robotsData = new DatosAgentes();
        boxesData = new DatosCaja();
        palletsData = new Tarimas();
        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();
        boxes = new Dictionary<string, GameObject>();
        robots = new Dictionary<string, GameObject>();
        pallets = new Dictionary<string, GameObject>();
        floor.transform.localScale = new Vector3((float)(width + 1) / 10, 1, (float)(height + 1) / 10);
        floor.transform.localPosition = new Vector3((float)width / 2 - 0.5f, 0, (float)height / 2 - 0.5f);
        timer = timeToUpdate;
        StartCoroutine(SendConfiguration());
    }
/// It sends a POST request to the server with the configuration data
      IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("NAgents", (NBoxes).ToString());
        form.AddField("width", (width).ToString());
        form.AddField("height", (height).ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            StartCoroutine(GetAgentesData());
            StartCoroutine(GetCajasData());
            StartCoroutine(GetTarimasData());
        }
    }
/// It gets the data from the server, and if it's successful, it updates the positions of the agents
    IEnumerator GetAgentesData()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getAgentsEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else
        {
            robotsData = JsonUtility.FromJson<DatosAgentes>(www.downloadHandler.text);

            foreach (RobotData rob in robotsData.positions)
            {
                Vector3 newAgentPosition = new Vector3(rob.x, rob.y, rob.z);

                if (!started)
                {
                    prevPositions[rob.id] = newAgentPosition;
                    robots[rob.id] = Instantiate(robot, newAgentPosition, Quaternion.identity);
                }
                else
                {
                    if (rob.hasBox)
                    {
                        robots[rob.id].GetComponent<RecogerCaja>().AddBox();
                    }
                    else
                    {
                        robots[rob.id].GetComponent<RecogerCaja>().RemoveBox();
                    }
                    Vector3 currentPosition = new Vector3();
                    if (currPositions.TryGetValue(rob.id, out currentPosition))
                        prevPositions[rob.id] = currentPosition;
                    currPositions[rob.id] = newAgentPosition;
                }
            }

            updated = true;
            if (!started) started = true;
        }
    }
/// It gets the data from the server, parses it into a BoxesData object, and then instantiates the boxes
/// in the scene
    IEnumerator GetCajasData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getCajasEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            boxesData = JsonUtility.FromJson<DatosCaja>(www.downloadHandler.text);

            foreach(DatosCajas cajita in boxesData.positions)
            {
                if (!startedBox)
                {
                    Vector3 boxPosition = new Vector3(cajita.x, cajita.y, cajita.z);
                    boxes[cajita.id] = Instantiate(caja, boxPosition, Quaternion.identity);
                }
                else
                {
                    if(cajita.picked_up){
                        boxes[cajita.id].SetActive(false);
                    }
                }
            }
            if (!startedBox) startedBox = true;
        }
    }
/// It gets the data from the server, parses it into a JSON object, and then instantiates the pallets
/// and boxes
    IEnumerator GetTarimasData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getTarimasEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            palletsData = JsonUtility.FromJson<Tarimas>(www.downloadHandler.text);

            foreach(DatosTarimas tarima in palletsData.positions)
            {
                if (!startedPallet)
                {
                    Vector3 palletPosition = new Vector3(tarima.x, tarima.y, tarima.z);
                    pallets[tarima.id] = Instantiate(pallet, palletPosition, Quaternion.identity);
                }
                else
                {
                    pallets[tarima.id].GetComponent<ApilaCajas>().AddBox(tarima.value);
                }
            }
            if (!startedPallet) startedPallet = true;
        }
    }

/// We're updating the position of the robots in the scene by interpolating between the previous and
/// current positions of the robots
    private void Update() 
    {
        if(timer < 0)
        {
            timer = timeToUpdate;
            updated = false;
            StartCoroutine(UpdateSimulation());
        }

        if (updated)
        {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            foreach(var rob in currPositions)
            {
                Vector3 currentPosition = rob.Value;
                Vector3 previousPosition = prevPositions[rob.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = currentPosition - interpolated;

                robots[rob.Key].transform.localPosition = interpolated;
                if(direction != Vector3.zero) robots[rob.Key].transform.rotation = Quaternion.LookRotation(direction);
            }
        }
    }
/// It updates the simulation.

    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            StartCoroutine(GetAgentesData());
            StartCoroutine(GetCajasData());
            StartCoroutine(GetTarimasData());
        }
    }
}
