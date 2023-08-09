# APRS Framework Neo4j Database Dumps

## Introduction

This repository holds the database dumps for the Faunc and Motoman robots' Neo4j databases, which play a crucial role in the APRS (Agility Performance of Robotic Systems) framework at the National Institute of Standards and Technology (NIST). The primary goal of this repository is to provide versioned backups of the databases, encourage collaboration among team members, and support the ongoing process of updating the database by incorporating new robots and relevant data.

## Table of Contents

- [Introduction](#introduction)
- [Database Information](#database-information)
- [Database Updates](#database-updates)
- [License](#license)

## Database Information

- **Database Format:** Neo4j
- **Included Robots:**
  - Faunc Robot
  - Motoman Robot

## Database Updates

As part of ongoing development and improvement of the database, the following updates are planned:

1. **Update Neo4j Version:** Upgrade the Neo4j database to the latest version. This ensures compatibility with new features and improvements introduced by Neo4j and helps maintain the security and performance of the database.

2. **Add New Robots:** Expand the database to include data for new robots that have been integrated into the APRS framework. This involves adding their kinematic parameters, joint configurations, and any other relevant information required for path planning and execution.

3. **Convert System to World Coordinates:** Implement a conversion of the system's internal coordinates to world coordinates. This conversion will enhance interoperability with external systems, facilitate data exchange, and support seamless integration with other software components.

4. **Updated Ontology Setup:** Update the documentation and notes to accurately reflect the current ontology setup within the database. As the ontologies evolve, ensure that the database schema and relationships align with the latest ontology definitions.

## License

This repository is licensed under the [Apache License 2.0](LICENSE), which means you're free to use, modify, and distribute the codebase under the terms of this license.
