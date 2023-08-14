from neo4j import GraphDatabase

class Neo4jManager:
    def __init__(self,URI,AUTH):
        self._driver = GraphDatabase.driver(URI,auth=AUTH)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def delete_single_pose(self,name):

        cypher = """
            MATCH (n { name:$name } ) -[r] - () 
            DELETE n,r
            """
        with self._driver.session(database="neo4j") as session:
            result = session.run(cypher,name=name)
            return result.data()
        
    def get_all_new_empty_slot_pose(self):

        cypher = """
            MATCH (o) WITH max(o.visioncycle) as maxvisioncycle
            MATCH (source)<-[:hasSkuObject_Sku]-(object)-[:hasSolidObject_PrimaryLocation]->(n)-[r2]->(pose:Pose)- [r1:hasPose_Point] -> (p:Point),
            (pose) - [r3:hasPose_XAxis] -> (xaxis:Vector),
            (pose) - [r4:hasPose_ZAxis] -> (zaxis:Vector)
            WHERE object.visioncycle > maxvisioncycle -2 and object.name =~ 'empty_slot.*'
            RETURN object.name as name,p.hasPoint_X as x,p.hasPoint_Y as y,p.hasPoint_Z as z, xaxis.hasVector_I as vxi,xaxis.hasVector_J as vxj,xaxis.hasVector_K as vxk, zaxis.hasVector_I as vzi,zaxis.hasVector_J as vzj,zaxis.hasVector_K as vzk, object.visioncycle as visioncycle, maxvisioncycle
            """

        with self._driver.session(database="neo4j") as session:
            result = session.run(cypher)
            return result.data()
        
    def get_all_new_pose(self):

        cypher = """
            MATCH (o) WITH max(o.visioncycle) as maxvisioncycle
            MATCH (sku:StockKeepingUnit)<-[:hasSkuObject_Sku]-(object)-[:hasSolidObject_PrimaryLocation]->(n)-[r2]->(pose:Pose)- [r1:hasPose_Point] -> (p:Point),
            (pose) - [r3:hasPose_XAxis] -> (xaxis:Vector),
            (pose) - [r4:hasPose_ZAxis] -> (zaxis:Vector)
            WHERE object.visioncycle > maxvisioncycle -2 
            RETURN object.name as name,p.hasPoint_X as x,p.hasPoint_Y as y,p.hasPoint_Z as z, xaxis.hasVector_I as vxi,xaxis.hasVector_J as vxj,xaxis.hasVector_K as vxk, zaxis.hasVector_I as vzi,zaxis.hasVector_J as vzj,zaxis.hasVector_K as vzk, object.visioncycle as visioncycle, maxvisioncycle,sku.name as sku_name
        """

        with self._driver.session(database="neo4j") as session:
            result = session.run(cypher)
            return result.data()

    def get_all_parts_in_pt(self, part_name):

        cypher = """
            MATCH (v) WITH max(v.visioncycle)-3 as maxv
            MATCH (partinpt:Part) where partinpt.name STARTS WITH $part_name and partinpt.visioncycle > maxv 
            RETURN partinpt.name as name
        """

        # MATCH partinkt = (n:Part) where n.name CONTAINS "in_kt" and n.visioncycle > maxv

        with self._driver.session(database="neo4j") as session:
            result = session.run(cypher,part_name=part_name)
            return result.data()
        
    def get_all_parts_in_kt(self, part_name):

        cypher = """
            MATCH (v) WITH max(v.visioncycle)-3 as maxv
            MATCH (partinkt:Part) where partinkt.name STARTS WITH $part_name and partinkt.visioncycle > maxv 
            RETURN partinkt.name as name
        """
        # MATCH (partinkt:Part) where partinkt.name CONTAINS "in_kt" and partinkt.visioncycle > maxv

        with self._driver.session(database="neo4j") as session:
            result = session.run(cypher,part_name=part_name)
            return result.data()
        
    def get_all_pose(self):

        cypher = """
            MATCH pointpath=(source)<-[:hasSkuObject_Sku]-(object)-[:hasSolidObject_PrimaryLocation]->(n)-[r2]->(pose:Pose)- [r1:hasPose_Point] -> (p:Point),
            (pose) - [r3:hasPose_XAxis] -> (xaxis:Vector),
            (pose) - [r4:hasPose_ZAxis] -> (zaxis:Vector)
            RETURN object.name as name,p.hasPoint_X as x,p.hasPoint_Y as y,p.hasPoint_Z as z, xaxis.hasVector_I as vxi,xaxis.hasVector_J as vxj,xaxis.hasVector_K as vxk, zaxis.hasVector_I as vzi,zaxis.hasVector_J as vzj,zaxis.hasVector_K as vzk, object.visioncycle as visioncycle
        """
        with self._driver.session(database="neo4j") as session:
            result = session.run(cypher)
            return result.data()          

    def get_partdesign_part_count(self,sku_part_name):

        cypher = """
            MATCH (n:StockKeepingUnit)-[:hasPartsTrayDesign_VesselSku]-(pd:PartsTrayDesign)-[hasPartsTrayDesign_PartRefAndPose]-(rap:PartRefAndPose) 
            WHERE n.name=$sku_part_name
            RETURN count(rap)
            """
        with self._driver.session(database="neo4j") as session:
            result = session.run(cypher,sku_part_name=sku_part_name)
            return result.data()  
        
    def get_partstrays(self,sku_part_name):

        cypher = """
            MATCH (n:StockKeepingUnit)-[:hasSkuObject_Sku]-(pt:PartsTray),
            (n)-[:hasStockKeepingUnit_ExternalShape]-(xshape),
            (pt)-[:hasPartsTray_Design]->(d:PartsTrayDesign)
            WHERE n.name=$sku_part_name
            RETURN pt.name as name, n.name as sku_name, ID(pt) as id, d.name as design, pt.hasPartsTray_Complete as complete
            """
        # The id function will be removed in the next major release. It is recommended to use elementId instead.
        with self._driver.session(database="neo4j") as session:
            result = session.run(cypher,sku_part_name=sku_part_name)
            return result.data()  

    def get_single_pose(self, part_name):

        cypher = """
            MATCH (o) WITH max(o.visioncycle) as maxvisioncycle
            MATCH pointpath=(object { name:$part_name } )-[:hasSolidObject_PrimaryLocation]->(n)-[r2]->(pose:Pose)- [r1:hasPose_Point] -> (p:Point),
            (pose) - [r3:hasPose_XAxis] -> (xaxis:Vector),
            (pose) - [r4:hasPose_ZAxis] -> (zaxis:Vector)
            RETURN object.name as name,p.hasPoint_X as x,p.hasPoint_Y as y,p.hasPoint_Z as z, xaxis.hasVector_I as vxi,xaxis.hasVector_J as vxj,xaxis.hasVector_K as vxk, zaxis.hasVector_I as vzi,zaxis.hasVector_J as vzj,zaxis.hasVector_K as vzk, object.visioncycle as visioncycle, maxvisioncycle
        """
        # MATCH (partinkt:Part) where partinkt.name CONTAINS "in_kt" and partinkt.visioncycle > maxv

        with self._driver.session(database="neo4j") as session:
            result = session.run(cypher,part_name=part_name)
            return result.data()
        
    def get_slots(self,part_tray_name):
     
        cypher = """
            MATCH (p:PartsTray)-[:hasPartsTray_Slot]-(s:Slot)-[:hasSlot_PartRefAndPose]-(prp:PartRefAndPose)-[:hasPartRefAndPose_Pose]-(pose:Pose)-[:hasPose_Point]-(point:Point), 
            (prp) - [:hasPartRefAndPose_Sku] -> (sku:StockKeepingUnit)-[:hasStockKeepingUnit_ExternalShape]-(xshape:ExternalShape)
            WHERE p.name=$part_tray_name
            RETURN s.name as name, s.hasSlot_IsOccupied as slot_occupied, s.hasSlot_ID as slot_id, sku.name as sku_name, point.hasPoint_X as x, point.hasPoint_Y as y, point.hasPoint_Z as z
            """

        with self._driver.session(database="neo4j") as session:
            result = session.run(cypher,part_tray_name=part_tray_name)
            return result.data()   

    def get_tray_slots_from_kit_sku(self,sku_part_tray_name):
     
        cypher = """
            MATCH (n:StockKeepingUnit)-[:hasSkuObject_Sku]-(p:PartsTray)-[:hasPartsTray_Slot]-(s:Slot)-[:hasSlot_PartRefAndPose]-(prp:PartRefAndPose)-[:hasPartRefAndPose_Pose]-(pose:Pose)-[:hasPose_Point]-(point:Point),
            (prp)-[:hasPartRefAndPose_Sku]->(sku:StockKeepingUnit)
            WHERE n.name=$sku_part_tray_name
            RETURN distinct ID(s) as nodeid, s.name as name, sku.name as skuname, point.hasPoint_X as x, point.hasPoint_Y as y
            """
        # The id function will be removed in the next major release. It is recommended to use elementId instead.
        with self._driver.session(database="neo4j") as session:
            result = session.run(cypher,sku_part_tray_name=sku_part_tray_name)
            return result.data()   

    def get_tray_slots(self,part_tray_name):
     
        cypher = """
            MATCH (p:PartsTray)-[:hasPartsTray_Slot]-(s:Slot)-[:hasSlot_PartRefAndPose]-(prp:PartRefAndPose)-[:hasPartRefAndPose_Pose]-(pose:Pose)-[:hasPose_Point]-(point:Point), 
            (prp) - [:hasPartRefAndPose_Sku] -> (sku:StockKeepingUnit)
            WHERE p.name=$part_tray_name
            OPTIONAL MATCH (sku) - [:hasStockKeepingUnit_InternalShape] -> (shape:CylindricalShape) 
            RETURN s.name as name, point.hasPoint_X as x, point.hasPoint_Y as y, sku.name as sku_name, prp.name as prp_name, p.name as tray_name,shape.hasCylindricalShape_Diameter as diameter
            """

        with self._driver.session(database="neo4j") as session:
            result = session.run(cypher,part_tray_name=part_tray_name)
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
    print("\n1. Get All Pose")
    print("2. Get All Parts in PT")
    print("3. Get All Parts in KT")
    print("4. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        pose = manager.get_all_pose()
        for part in pose:
            print(part["name"])
    elif choice == "2":
        part_name = input("Enter Starting of Part Name: ")
        parts = manager.get_all_parts_in_pt(part_name)
        print("Parts in Part Tray Are:")
        for part in parts:
            print(part)
    elif choice == "3":
        part_name = input("Enter Starting of Part Name: ")
        parts = manager.get_all_parts_in_kt(part_name)
        print("Parts in Kit Tray Are:")
        for part in parts:
            print(part)
    elif choice == "4":
        manager.close()
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please select again.")
