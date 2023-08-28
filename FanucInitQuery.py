from neo4j import GraphDatabase

class Neo4jManager:
    def __init__(self,URI,AUTH):
        self._driver = GraphDatabase.driver(URI,auth=AUTH)
        self._driver.verify_connectivity()


    def close(self):
        self._driver.close()
        
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
            dict1 = result.data()
            print("\n{:<20} {:<20} {:<5} {:<25} {:<20}".format('NAME','SKU_NAME','ID','DESIGN','COMPLETE'))
            for result_dict in dict1:
                name = result_dict["name"]
                sku_name = result_dict['sku_name']
                id = result_dict['id']
                design = result_dict['design']
                complete = result_dict['complete']
                print("{:<20} {:<20} {:<5} {:<25} {:<20}".format(name,sku_name,id,design,complete))
        
    def get_slots(self,part_tray_name):
     
        cypher = """
            MATCH (p:PartsTray)-[:hasPartsTray_Slot]-(s:Slot)-[:hasSlot_PartRefAndPose]-(prp:PartRefAndPose)-[:hasPartRefAndPose_Pose]-(pose:Pose)-[:hasPose_Point]-(point:Point), 
            (prp) - [:hasPartRefAndPose_Sku] -> (sku:StockKeepingUnit)-[:hasStockKeepingUnit_ExternalShape]-(xshape:ExternalShape)
            WHERE p.name=$part_tray_name
            RETURN s.name as name, s.hasSlot_IsOccupied as slot_occupied, s.hasSlot_ID as slot_id, sku.name as sku_name, point.hasPoint_X as x, point.hasPoint_Y as y, point.hasPoint_Z as z
            """

        with self._driver.session(database="neo4j") as session:
            result = session.run(cypher,part_tray_name=part_tray_name)
            dict1 = result.data()
            print("\n{:<20} {:<20} {:<5} {:<25} {:<20} {:<20} {:<20}".format('NAME','SLOT_OCCUPIED','SLOT_ID','SKU_NAME','X','Y','Z'))
            for result_dict in dict1:
                name = result_dict["name"]
                sku_name = result_dict['sku_name']
                x = result_dict['x']
                y = result_dict['y']
                z = result_dict['z']
                slot_occupied = result_dict['slot_occupied']
                slot_id = result_dict['slot_id']
                print("{:<20} {:<20} {:<5} {:<25} {:<20} {:<20} {:<20}".format(name,slot_occupied,slot_id,sku_name,x,y,z))  

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
            dict1 = result.data()
            print("\n{:<30} {:<15} {:<15} {:<25} {:<42} {:<20} {:<15}".format('NAME','X','Y','SKU_NAME','PRP_NAME','TRAY_NAME','DIAMETER'))
            for result_dict in dict1:
                name = result_dict["name"]
                sku_name = result_dict['sku_name']
                x = result_dict['x']
                y = result_dict['y']
                prp_name = result_dict['prp_name']
                tray_name = result_dict['tray_name']
                diameter = result_dict['diameter']
                print("{:<30} {:<15} {:<15} {:<25} {:<42} {:<20} {:<15}".format(name,x,y,sku_name,prp_name,tray_name,diameter))  

with open('Neo4j-Credentials.txt') as f:
    contents = f.readlines()
    URI = contents[1].split("=")[1].rstrip('\n')
    USERNAME = contents[2].split("=")[1].rstrip('\n')
    PASSWORD = contents[3].split("=")[1].rstrip('\n')
    AUTH = (USERNAME,PASSWORD)
    f.close

manager = Neo4jManager(URI,AUTH)

#getPartsTrays_.....
manager.get_partstrays('sku_kit_m2l1_vessel')

#getSlotOffsetsNew_....
manager.get_tray_slots("kit_m2l1_vessel_1")
manager.get_tray_slots("kit_s2l2_vessel_1")
manager.get_tray_slots("large_gear_vessel_1")
manager.get_tray_slots("medium_gear_vessel_1")
manager.get_tray_slots("small_gear_vessel_1")

#getSlots_....
manager.get_slots('kit_m2l1_vessel_1')
manager.get_slots('kit_m2l1_vessel_2')

manager.close()
