# SectionAnalysisTool

Ver: 0.0.1
    Alpha phase - tool can now handle inhomogeneous sections
    
Ver: 0.0.0
	Alpha phase - created tool and have done some testing. Cleaned up the GUI and ready to trial.
	
This is a simply static analysis program for cross sections. A complete explanation of the tool can be found in the user guide. In short, the tool takes in a given simple polygon with a given load and calculates stresses at key locatins. Key locations include the vertices of the polygon and points along their edges.

The polygon can be made up from other polygons. A section can consist of rectangles, circle segments and polygons. Each item added to the section can have a different modulus or stiffness. This stiffness changes the distribution of stress and represents inhomogenous sections.
