using System.Collections;
using System.Collections.Generic;
using UnityEngine;

/*# ----------------------------------------------------------
# Actividad Integradora ApilaCajas.cs
#
# Date: 21-Nov-2022
# Authors:
#           Sergio Manuel Gonzalez Vargas - A01745446
#           Gilberto André García Gaytán - A01753176
#           Fernando Ortiz Saldaña - A01376737
#           Ricardo Ramírez Condado - A01379299
# ----------------------------------------------------------*/

/* It activates the box that corresponds to the number of the counter */
public class ApilaCajas : MonoBehaviour
{
    public GameObject caja1, caja2, caja3, caja4, caja5;
    // Start is called before the first frame update
    /// This function is used to disable the boxes at the start of the game
    void Start()
    {
        caja1.SetActive(false);
        caja2.SetActive(false);
        caja3.SetActive(false);
        caja4.SetActive(false);
        caja5.SetActive(false);
    }

/// It activates the box that corresponds to the number of the counter
/// <param name="contador">This is the number of boxes that have been collected.</param>
    public void AddBox(int contador)
    {
        if (contador == 1)
        {
            caja1.SetActive(true);
        }
        else if (contador == 2)
        {
            caja2.SetActive(true);
        }
        else if (contador == 3)
        {
            caja3.SetActive(true);
        }
        else if (contador == 4)
        {
            caja4.SetActive(true);
        }
        else if (contador == 5)
        {
            caja5.SetActive(true);
        }
    }
}
