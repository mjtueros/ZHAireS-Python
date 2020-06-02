#!/usr/bin/env python
import sys
import h5py

namelist=[]
def put_datasets_on_namelist(name,node):
    if isinstance(node, h5py.Dataset):
         # node is a dataset
         namelist.append(name)
         #print("putting datasset " + name)
    #else:
         # node is a group
         #print("skipping group " + name)

def RemoveTableFromHDF5(InputFilename,OutputFilename,TableName):

    print("Coping everything exept "+str(TableName)+" from " + str(InputFilename) + " to " + str(OutputFilename))
    fs = h5py.File(InputFilename, 'r')
    fd = h5py.File(OutputFilename, 'a')

    fs.visititems(put_datasets_on_namelist)

    for name in namelist:
      if not TableName in name:
        # Get the name of the parent for the group we want to copy
        group_path = fs[name].parent.name
        # Check that this group exists in the destination file; if it doesn't, create it
        # This will create the parents too, if they don't exist
        group_id = fd.require_group(group_path)
        #copy the element to the relevant location
        fs.copy(name,group_id)
     # else:
        #print("skipping "+str(name))


if __name__ == '__main__':

  if (len(sys.argv)>4 or len(sys.argv)<3) :
    print("Usage: RemoveTable InputFilename OutputFilename TableName")

  else :
    InputFilename=sys.argv[1]
    OutputFilename=sys.argv[2]
    TableName=sys.argv[3]
    RemoveTableFromHDF5(InputFilename,OutputFilename,TableName)


