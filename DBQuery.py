from neo4j import GraphDatabase

class Neo4jManager:
    def __init__(self,URI,AUTH):
        self._driver = GraphDatabase.driver(URI,auth=AUTH)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()
        
    def get_all_pose(self):
        cypher = """
            MATCH pointpath=(source)<-[:hasSkuObject_Sku]-(object)-[:hasSolidObject_PrimaryLocation]->(n)-[r2]->(pose:Pose)- [r1:hasPose_Point] -> (p:Point),
            xaxispath= (pose) - [r3:hasPose_XAxis] -> (xaxis:Vector),
            zaxispath= (pose) - [r4:hasPose_ZAxis] -> (zaxis:Vector)
            RETURN object.name as name,p.hasPoint_X as x,p.hasPoint_Y as y,p.hasPoint_Z as z, xaxis.hasVector_I as vxi,xaxis.hasVector_J as vxj,xaxis.hasVector_K as vxk, zaxis.hasVector_I as vzi,zaxis.hasVector_J as vzj,zaxis.hasVector_K as vzk, object.visioncycle as visioncycle
        """
        with self._driver.session(database="neo4j") as session:
            result = session.run(cypher)
            return result.data()
        
    def get_all_parts_in_pt(self, part_name):

        cypher = """
            MATCH (v) with max(v.visioncycle)-3 as maxv
            MATCH partinpt = (n:Part) where n.name STARTS WITH $part_name and n.visioncycle > maxv 
            RETURN n.name as name
        """

        with self._driver.session(database="neo4j") as session:
            result = session.run(cypher,part_name=part_name)
            return result.data()
        

with open('Neo4j-Credentials.txt') as f:
    contents = f.readlines()
    URI = contents[1].split("=")[1].rstrip('\n')
    USERNAME = contents[2].split("=")[1].rstrip('\n')
    PASSWORD = contents[3].split("=")[1].rstrip('\n')
    AUTH = (USERNAME,PASSWORD)
    f.close

manager = Neo4jManager(URI,AUTH)

while True:
    print("1. Get All Pose")
    print("2. Get All Parts in PT")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        pose = manager.get_all_pose()
        for part in pose:
            print(part["name"])
    elif choice == "2":
        part_name = input("Enter Starting of Part Name: ")
        parts = manager.get_all_parts_in_pt(part_name)
        print(len(parts))
        for part in parts:
            print(part)
    elif choice == "3":
        manager.close()
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please select again.")
