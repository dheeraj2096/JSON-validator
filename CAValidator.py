import sys
import json

flag = False

def validate_instance(input_schema,input_instance):
    global flag
    if type(input_instance) == dict:
        for key,value in input_instance.items():
            if 'name' in input_schema.keys() and key == input_schema['name']:
#                print("Name match at "+ key)
                if input_schema['cardinality'] == 'n':
                    if 'composite' in input_schema.keys():
                        if type(value) == list:
                            for part_value in value:
                                value_dict = [{x:y} for x,y in part_value.items()]
                                for index_value,composite_value in enumerate(input_schema['composite']):
                                    validate_instance(composite_value,value_dict[index_value])
                    elif 'simple' in input_schema.keys():
                        for part_value in value:
                            if type(part_value) != myDictionary[input_schema['simple']]:
                                print("Value Mismatch at "+ str(part_value))
                                flag = True
                            else:
#                                print("Value match at "+str(part_value))
                                pass
                else:
                    if 'composite' in input_schema.keys():
                        if type(value) == dict:
                            value_dict = [{x:y} for x,y in value.items()]
                            for index_value,composite_value in enumerate(input_schema['composite']):
                                validate_instance(composite_value,value_dict[index_value])
                    elif 'simple' in input_schema.keys():
                        if type(value) == myDictionary[input_schema['simple']]:
#                            print("Value match at "+str(value))            
                             pass               
                        else:
                            print("Value Mismatch at " + str(value))
                            flag = True
            else:
                print("Name Mismatch at "+key)
                flag = True
                
myDictionary = {
    "integer":int,
    "string":str,
    "decimal":float
}

def main():
    with open(sys.argv[1]) as f:
        schema = json.load(f)
    with open(sys.argv[2]) as f:
        instance = json.load(f)
    global flag
    validate_instance(schema,instance)
    if flag == False:
        print(sys.argv[2]+" conforms to schema in "+sys.argv[1])
    else:
        print(sys.argv[2]+" does not conforms to schema in "+sys.argv[1])

if __name__=="__main__":
    main()