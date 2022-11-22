using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/*# ----------------------------------------------------------
# Actividad Integradora RecogerCaja.cs
#
# Date: 21-Nov-2022
# Authors:
#           Sergio Manuel Gonzalez Vargas - A01745446
#           Gilberto André García Gaytán - A01753176
#           Fernando Ortiz Saldaña - A01376737
#           Ricardo Ramírez Condado - A01379299
# ----------------------------------------------------------*/

/* This class is used to control the box and the light */
public class RecogerCaja : MonoBehaviour
{/* Declaring the variables Box and Luz. */

    public GameObject Box;
    public Light Luz;
    
    // Start is called before the first frame update
/// This function is called when the script is loaded. It sets the box to be invisible and the light to
/// be yellow
    void Start()
    {
        Box.SetActive(false);
        Luz.color = Color.yellow;
    }
/// > This function removes the box from the scene and 
/// changes the color of the light to yellow
    public void RemoveBox()
    {
        Box.SetActive(false);
        Luz.color = Color.yellow;
    }

/// It sets the box to active and changes the color of the light to blue.
    public void AddBox()
    {
        Box.SetActive(true);
        Luz.color = Color.blue;
    }
}
