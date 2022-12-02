using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CityMaker : MonoBehaviour
{
    /* Declaring the variables. */
    [SerializeField] TextAsset layout;
    [SerializeField] GameObject roadPrefab;
    [SerializeField] GameObject buildingPrefab;
    [SerializeField] GameObject semaphorePrefab;
    [SerializeField] int tileSize;
    
    public List<GameObject> Semaforo;
    public static CityMaker Instance;

    // Start is called before the first frame update
    void Start()
    {
    	Instance = this;
        MakeTiles(layout.text);
        ControlaLuces();
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    
    /// "Turn on the third child of each of the 28 objects in the Semaforo array."
    /// The above function is called from the Update() function.
    void ControlaLuces() {
    	Semaforo[0].transform.GetChild(2).gameObject.SetActive(true);
    	Semaforo[1].transform.GetChild(2).gameObject.SetActive(true);
    	Semaforo[2].transform.GetChild(0).gameObject.SetActive(true);
    	Semaforo[3].transform.GetChild(0).gameObject.SetActive(true);
    	Semaforo[4].transform.GetChild(2).gameObject.SetActive(true);
    	Semaforo[5].transform.GetChild(2).gameObject.SetActive(true);
    	Semaforo[6].transform.GetChild(2).gameObject.SetActive(true);
    	Semaforo[7].transform.GetChild(2).gameObject.SetActive(true);
    	Semaforo[8].transform.GetChild(0).gameObject.SetActive(true);
    	Semaforo[9].transform.GetChild(0).gameObject.SetActive(true);
    	Semaforo[10].transform.GetChild(0).gameObject.SetActive(true);
    	Semaforo[11].transform.GetChild(0).gameObject.SetActive(true);
    	Semaforo[12].transform.GetChild(0).gameObject.SetActive(true);
    	Semaforo[13].transform.GetChild(0).gameObject.SetActive(true);
    	Semaforo[14].transform.GetChild(0).gameObject.SetActive(true);
    	Semaforo[15].transform.GetChild(0).gameObject.SetActive(true);
    	Semaforo[16].transform.GetChild(2).gameObject.SetActive(true);
    	Semaforo[17].transform.GetChild(2).gameObject.SetActive(true);
    	Semaforo[18].transform.GetChild(2).gameObject.SetActive(true);
    	Semaforo[19].transform.GetChild(2).gameObject.SetActive(true);
    	Semaforo[20].transform.GetChild(2).gameObject.SetActive(true);
    	Semaforo[21].transform.GetChild(2).gameObject.SetActive(true);
    	Semaforo[22].transform.GetChild(0).gameObject.SetActive(true);
    	Semaforo[23].transform.GetChild(0).gameObject.SetActive(true);
    	Semaforo[24].transform.GetChild(0).gameObject.SetActive(true);
    	Semaforo[25].transform.GetChild(0).gameObject.SetActive(true);
    	Semaforo[26].transform.GetChild(2).gameObject.SetActive(true);
    	Semaforo[27].transform.GetChild(2).gameObject.SetActive(true);
    }
    void MakeTiles(string tiles)
    {
        int x = 0;
        // Mesa has y 0 at the bottom
        // To draw from the top, find the rows of the file
        // and move down
        // Remove the last enter, and one more to start at 0
        int y = tiles.Split('\n').Length - 2;
        Debug.Log(y);

        Vector3 position;
        Vector3 positionSemaforo;
        GameObject tile;

        /* The above code is creating a city. */
        for (int i=0; i<tiles.Length; i++) {
            if (tiles[i] == '>' || tiles[i] == '<') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'v' || tiles[i] == '^') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 's') {
                positionSemaforo = new Vector3((x * tileSize)+0.45f, 0, y * tileSize);
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                tile = Instantiate(semaphorePrefab, positionSemaforo, Quaternion.identity);
                tile.transform.parent = transform;
                Semaforo.Add(tile);
                x += 1;
            } else if (tiles[i] == 'S') {
                positionSemaforo = new Vector3((x * tileSize)+0.45f, 0, y * tileSize);
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                tile = Instantiate(semaphorePrefab, positionSemaforo, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                Semaforo.Add(tile);
                x += 1;
            } else if (tiles[i] == 'D') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(buildingPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.GetComponent<Renderer>().materials[0].color = Color.red;
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '#') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(buildingPrefab, position, Quaternion.identity);
                tile.transform.localScale = new Vector3(1, Random.Range(0.5f, 2.0f), 1);
                tile.transform.parent = transform;
                x += 1;
            } 
             else if (tiles[i] == '.') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(buildingPrefab, position, Quaternion.identity);
                tile.transform.localScale = new Vector3(1, Random.Range(0.5f, 2.0f), 1);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '\n') {
                x = 0;
                y -= 1;
            }
        }
    }
}
