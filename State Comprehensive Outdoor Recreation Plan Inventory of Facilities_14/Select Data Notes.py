#!/usr/bin/python

#Notes for Selecting out GoRI Data into SCOrP_Filtered 
#SPSS
Select IF OwnerTyp ='STA' OR
	(Trails Available) = 1 OR
	(Track and Field) = 1 OR
	(Beach Available) = 1 OR
	(Boating Allowed) = 1 OR
	(Pool Available) = 1 OR

#python?
if 'STA' in OwnerTyp:
            writer.writerow(flag + ['GoRI'])
    elif 1 in Trails Available:
            writer.writerow(flag + ['GoRI'])
    elif 1 in  Track and Field = 1
    		writer.writerow(flag + ['GoRI'])
    elif 1 in Beach Available = 1
   			writer.writerow(flag + ['GoRI'])
    elif 1 in Boating Allowed = 1 
   			writer.writerow(flag + ['GoRI'])
    elif 1 in Pool Available
   			writer.writerow(flag + ['GoRI'])
    else: 
        delete

#ADD Data from RIDOTbike15?
	#Select IF (Type) = 'PATH' OR 'STATEWIDE ROUTE'