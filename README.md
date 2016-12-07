# SectionAnalysisTool

Ver: 0.0.1
    Alpha phase - tool can now handle inhomogeneous sections
    
Ver: 0.0.0
	Alpha phase - created tool and have done some testing. Cleaned up the GUI and ready to trial.
	
This is a simply static analysis program for cross sections. A complete explanation of the tool can be found in the user guide. In short, the tool takes in a given simple polygon with a given load and calculates stresses at key locatins. Key locations include the vertices of the polygon and points along their edges.

The polygon can be made up from other polygons. A section can consist of rectangles, circle segments and polygons. Each item added to the section can have a different modulus or stiffness. This stiffness changes the distribution of stress and represents inhomogenous sections.

Lessons Learned:

I should have created one more class, a manager class which handles reanalysis and stress points as well as the stress field. The SectionAnalysis class should have just been to add/remove and calculate section properties and renamed to SectionProperties. SectionAnalysis should have then been to do the analysis of grid points and have a variable called changed so that it would only re-do the analysis if there was a change to the properties or the loads.
    
I also should have created the GUI file as a class and done it in a more OOP manner, however at the time of the creation, it was my first Python GUI and so I had no idea of the normal conventions. I have determined though that I'm likely going to refactor the code at this point since if I did I would probably just write it all in Java.
