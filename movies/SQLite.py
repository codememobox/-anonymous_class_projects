########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv
#################################################################################

## Change to False to disable Sample
SHOW = False

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
    
        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "azhou90"
        return gt_username
    
    # Part a.i Create Tables [2 points]
    def part_ai_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_1_sql = '''
            CREATE TABLE movies(
                     id INT,
                     title TEXT,
                     score REAL
            );
        '''
        ######################################################################
        
        return self.execute_query(connection, part_ai_1_sql)

    def part_ai_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_ai_2_sql = '''
            CREATE TABLE movie_cast(
                     movie_id INT,
                     cast_id INT,
                     cast_name TEXT,
                     birthday TEXT,
                     popularity REAL
            );        
        '''
        ######################################################################
        
        return self.execute_query(connection, part_ai_2_sql)
    
    # Part a.ii Import Data [2 points]
    def part_aii_1(self,connection,path):
        ############### CREATE IMPORT CODE BELOW ############################
        with open(path) as file:
            read = csv.reader(file, delimiter=',')
            for row in read:
                insert_records = ''' INSERT INTO movies VALUES(?,?,?)'''
                connection.execute(insert_records,row)
                connection.commit()
       ######################################################################
        
        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
    def part_aii_2(self,connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        with open(path) as file:
            read = csv.reader(file, delimiter=',')
            for row in read:
                insert_records = ''' INSERT INTO movie_cast VALUES(?,?,?,?,?)'''
                connection.execute(insert_records,row)
                connection.commit()
        ######################################################################
        
        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part a.iii Vertical Database Partitioning [5 points]
    def part_aiii(self,connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_aiii_sql = '''
            CREATE TABLE cast_bio(
                     cast_id INT,
                     cast_name TEXT,
                     birthday TEXT,
                     popularity REAL
            );
        '''
        ######################################################################
        
        self.execute_query(connection, part_aiii_sql)
        
        ############### CREATE IMPORT CODE BELOW ############################
        part_aiii_insert_sql = '''
            INSERT INTO cast_bio(
                     cast_id,
                     cast_name,
                     birthday,
                     popularity)
            SELECT DISTINCT mc.cast_id, mc.cast_name, mc.birthday, mc.popularity
            FROM movie_cast mc;
    
        '''
        ######################################################################
        
        self.execute_query(connection, part_aiii_insert_sql)
        
        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
       

    # Part b Create Indexes [1 points]
    def part_b_1(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_1_sql = '''
            CREATE INDEX movie_index
            ON movies(id);
        '''
        ######################################################################
        return self.execute_query(connection, part_b_1_sql)
    
    def part_b_2(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_2_sql =  '''
            CREATE INDEX cast_index
            ON movie_cast(cast_id);
        '''
        ######################################################################
        return self.execute_query(connection, part_b_2_sql)
    
    def part_b_3(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_b_3_sql = '''
            CREATE INDEX cast_bio_index
            ON cast_bio(cast_id);
        '''
        ######################################################################
        return self.execute_query(connection, part_b_3_sql)
    
    # Part c Calculate a Proportion [3 points]
    def part_c(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_c_sql = '''
        SELECT printf(
            '%.2f', 100*CAST(COUNT(id) AS FLOAT)/
                      CAST((SELECT COUNT(id) FROM movies) AS FLOAT)
                      ) 
                AS Proportion
        FROM movies m
        WHERE m.score > 50 AND LOWER(m.title) LIKE '%war%';
        '''
        ######################################################################
        cursor = connection.execute(part_c_sql)
        return cursor.fetchall()[0][0]

    # Part d Find the Most Prolific Actors [4 points]
    def part_d(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_d_sql = '''
            SELECT 
                cast_name,
                COUNT(popularity)  AS appearance_count
            FROM movie_cast
            WHERE popularity>10
            GROUP BY cast_name
            ORDER BY appearance_count DESC, cast_name
            LIMIT 5;
                
        '''
        ######################################################################
        cursor = connection.execute(part_d_sql)
        return cursor.fetchall()

    # Part e Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_e(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        # part_e_sql = '''
        #     SELECT
        #         m.title AS movie_title,
        #         printf('%.2f', m.score) AS movie_score,
        #         COUNT(mc.cast_id) AS cast_count
        #     FROM movies m INNER JOIN movie_cast mc
        #         ON m.id = mc.movie_id
        #     GROUP BY movie_title
        #     ORDER BY movie_score DESC, cast_count ASC, movie_title ASC
        #     LIMIT 5;                   
        # '''
        
        part_e_sql = '''
        SELECT
        movie_title,
        printf('%.2f',movie_score) AS movie_score,
        cast_count
        FROM
            (SELECT m.title AS movie_title,
                        m.score AS movie_score,
                        ct.cast_count AS cast_count
                FROM
                (SELECT
                movie_id,
                COUNT(*) AS cast_count
                FROM movie_cast
                GROUP BY movie_id) ct
                INNER JOIN (SELECT id, score,title FROM movies)  m
                ON ct.movie_id = m.id
            ORDER BY m.score DESC, cast_count ASC, movie_title ASC)
            LIMIT 5;                   
        '''        


        
        
        ######################################################################
        cursor = connection.execute(part_e_sql)
        return cursor.fetchall()
    
    # Part f Get High Scoring Actors [4 points]
    def part_f(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        # part_f_sql = '''
        #     SELECT
        #         mc.cast_id AS cast_id,
        #         mc.cast_name AS cast_name,
        #         printf('%.2f', AVG(score)) AS average_score
        #     FROM movies m INNER JOIN movie_cast mc
        #         ON m.id = mc.movie_id
        #     WHERE m.score >=25
        #     GROUP BY cast_id
        #     HAVING COUNT(movie_id)=1
        #     ORDER BY average_score DESC, cast_name 
        #     LIMIT 10;
        # '''
        part_f_sql = '''
        SELECT cast_id, cast_name, printf('%.2f',AVG(score)) AS average_score 
        FROM movie_cast INNER JOIN movies 
        ON movie_cast.movie_id = movies.id WHERE score>=25 
        GROUP BY cast_id 
        HAVING COUNT(cast_id)>2 
        ORDER BY AVG(score) DESC, cast_name 
        LIMIT 10;
        '''
        ######################################################################
        cursor = connection.execute(part_f_sql)
        return cursor.fetchall()

    # Part g Creating Views [6 points]
    def part_g(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_sql = '''
          CREATE VIEW good_collaboration AS 
              SELECT cast_member_id1,
                      cast_member_id2,
                       AVG(score) AS average_movie_score,
                       COUNT(score) AS movie_count
              FROM
                  (SELECT cast_member_id1,
                      cast_member_id2,
                      movies.score AS score
                  FROM (SELECT a.movie_id,cast_member_id1,cast_member_id2 
                            FROM (SELECT cast_id AS cast_member_id1,
                                              movie_id FROM movie_cast)  a 
                  INNER JOIN (SELECT cast_id AS cast_member_id2,
                                      movie_id FROM movie_cast)  b
                  ON (cast_member_id1<cast_member_id2 and a.movie_id==b.movie_id))  com
                  INNER JOIN movies ON com.movie_id = movies.id)
                  GROUP BY cast_member_id1, cast_member_id2 
                  HAVING  AVG(score)>=40 and movie_count>2;
          '''
        
        # part_g_sql = '''
        #     WITH table1 AS(
        #         SELECT
        #             mc1.cast_id AS cast_member_id1,
        #             mc1.cast_name AS cast_member_name1,
        #             mc2.cast_id AS cast_member_id2,
        #             mc2.cast_name AS cast_member_name2,
        #             m.id AS id,
        #             m.score AS score
        #         FROM movie_cast mc1 LEFT JOIN movie m ON mc1.movie_id = m.id
        #             LEFT JOIN movie_cast mc2 ON m.id = mc2.movie_id)
        #     CREATE VIEW good_collaboration AS(
        #         SELECT cast_member_id1,cast_member_id2,cast_member_name1,cast_member_name2,
        #             COUNT(id) OVER(PARTITION BY cast_member_id1, cast_member_id2) AS movie_count,
        #             AVG(score) OVER(PARTITION BY cast_member_id1, cast_member_id2) AS average_movie_score
        #     FROM(SELECT t1.cast_member_id1,t1.cast_member_id2,t1.id, t1.score
        #         FROM table1 t1
        #         WHERE t1.cast_member_id1 > ( SELECT t2.cast_member_id1
        #                                     FROM table1 t2
        #                                     WHERE t1.cast_member_id1=t2.cast_member_id2)
        #             )
        #     WHERE average_movie_score >=40 AND movie_count>=3;
        # '''

        # part_g_sql = '''
        # CREATE VIEW good_collaboration AS
        #         SELECT mc1.cast_id AS cast_member_id1,
        #         mc2.cast_id AS cast_member_id2, 
        #         COUNT(*) AS movie_count, 
        #         AVG(score) AS average_movie_score 
        #         FROM movie_cast mc1
        #         JOIN movie_cast mc2
        #         ON mc1.movie_id=mc2.movie_id
        #         JOIN movies 
        #         ON mc1.movie_id=movies.id
        #         WHERE cast_member_id1<cast_member_id2
        #         GROUP BY cast_member_id1,cast_member_id2 
        #         HAVING COUNT(*)>2 AND AVG(score)>=40;
        
        # '''

        
        ######################################################################
        return self.execute_query(connection, part_g_sql)
    
    def part_gi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_g_i_sql ='''
            SELECT j.cast_person AS cast_id,
                cast_name,
                printf('%.2f', AVG(average_movie_score)) AS collaboration_score
            FROM(SELECT cast_member_id1 AS cast_person,
                      average_movie_score
                FROM good_collaboration
                UNION ALL
                SELECT cast_member_id2 AS cast_person,
                    average_movie_score
                FROM good_collaboration
                ) j
            INNER JOIN (SELECT cast_id, cast_name FROM movie_cast) mc
            ON j.cast_person = mc.cast_id
            GROUP BY cast_id
            ORDER BY collaboration_score DESC, cast_name 
            LIMIT 5;
        
        '''
        # part_g_i_sql = '''
        #     SELECT cast_member_id1 AS cast_id,
        #         cast_member_name1 AS cast_name,
        #         printf('%.2f', average_movie_score) AS collaboration_score
        #     FROM good_collaboration
        #     ORDER BY collaboration_score DESC
        #     LIMIT 5
        # '''
        # part_g_i_sql = '''
        # SELECT cast_id, cast_name, printf('%.2f', AVG(average_movie_score) AS collaboration_score) 
        #     FROM (
        #         SELECT * FROM (SELECT cast_member_id1 AS cast_id,
        #                         name1 as cast_name, 
        #                         average_movie_score 
        #                         FROM good_collaboration) AS a
        #         INNER JOIN
        #         SELECT * FROM (SELECT cast_member_id2 AS cast_id, 
        #                         name2 AS cast_name,
        #                         average_movie_score 
        #                         FROM good_collaboration ) AS b
        #         ) ON a.cast_id=b.cast_id
        # GROUP BY cast_id 
        # ORDER BY collaboration_score DESC, cast_name ASC 
        # LIMIT 5;
        # '''
        # part_g_i_sql = '''
        #     SELECT j.cast_person AS cast_id, 
        #             cast_name, 
        #             printf('%.2f',AVG(average_movie_score)) AS collaboration_score 
        #         FROM (SELECT 
        #                       cast_member_id1 AS cast_person,
        #                       average_movie_score
        #                       FROM good_collaboration
        #           UNION ALL
        #               SELECT 
        #                       cast_member_id2 AS cast_person,
        #                       average_movie_score
        #                       FROM good_collaboration) AS j
        #         INNER JOIN (SELECT cast_id,cast_name FROM movie_cast) AS mc
        #         ON j.cast_person = mc.cast_id
        #         GROUP BY cast_id
        #         ORDER BY printf('%.2f',AVG(average_movie_score)) DESC, cast_name ASC
        #         LIMIT 5;
        # '''

        
        
        
        ######################################################################
        cursor = connection.execute(part_g_i_sql)
        return cursor.fetchall()
    
    # Part h FTS [4 points]
    def part_h(self,connection,path):
        ############### EDIT SQL STATEMENT ###################################
        part_h_sql = '''
        CREATE VIRTUAL TABLE movie_overview USING fts3( id INTEGER, overview TEXT);
        '''
        ######################################################################
        connection.execute(part_h_sql)
        ############## CREATE IMPORT CODE BELOW ############################
        with open(path, encoding='utf-8-sig') as file:
            read = csv.reader(file, quotechar='"', 
                              delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
            for row in read:
                insert_records = ''' INSERT INTO movie_overview VALUES(?,?)'''
                connection.execute(insert_records,row)
                connection.commit()
        
        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
        
    def part_hi(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hi_sql = '''
            SELECT COUNT(*) 
            FROM movie_overview 
            WHERE movie_overview.overview MATCH "fight";
        '''
        ######################################################################
        cursor = connection.execute(part_hi_sql)
        return cursor.fetchall()[0][0]
    
    def part_hii(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_hii_sql = '''
            SELECT COUNT(*) 
            FROM movie_overview 
            WHERE movie_overview.overview MATCH "space NEAR/5 program";
        '''
        ######################################################################
        cursor = connection.execute(part_hii_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":
    
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except:
        print("Error in Table Drops")

    # try:
    #     print('\033[32m' + "part ai 1: " + '\033[m' + str(db.part_ai_1(conn)))
    #     print('\033[32m' + "part ai 2: " + '\033[m' + str(db.part_ai_2(conn)))
    # except:
    #       print("Error in Part a.i")

    # try:
    #     print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_aii_1(conn,"data/movies.csv")))
    #     print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(db.part_aii_2(conn,"data/movie_cast.csv")))
    # except:
    #     print("Error in part a.ii")

    # try:
    #     print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_aiii(conn)))
    # except:
    #     print("Error in part a.iii")

    # try:
    #     print('\033[32m' + "part b 1: " + '\033[m' + db.part_b_1(conn))
    #     print('\033[32m' + "part b 2: " + '\033[m' + db.part_b_2(conn))
    #     print('\033[32m' + "part b 3: " + '\033[m' + db.part_b_3(conn))
    # except:
    #     print("Error in part b")

    # try:
    #     print('\033[32m' + "part c: " + '\033[m' + str(db.part_c(conn)))
    # except:
    #     print("Error in part c")

    # try:
    #     print('\033[32m' + "part d: " + '\033[m')
    #     for line in db.part_d(conn):
    #         print(line[0],line[1])
    # except:
    #     print("Error in part d")

    # try:
    #     print('\033[32m' + "part e: " + '\033[m')
    #     for line in db.part_e(conn):
    #         print(line[0],line[1],line[2])
    # except:
    #     print("Error in part e")

    # try:
    #     print('\033[32m' + "part f: " + '\033[m')
    #     for line in db.part_f(conn):
    #         print(line[0],line[1],line[2])
    # except:
    #     print("Error in part f")
    
    # try:
    #     print('\033[32m' + "part g: " + '\033[m' + str(db.part_g(conn)))
    #     print('\033[32m' + "part g.i: " + '\033[m')
    #     for line in db.part_gi(conn):
    #         print(line[0],line[1],line[2])
    # except:
    #     print("Error in part g")

    try:
        print('\033[32m' + "part h.i: " + '\033[m'+ str(db.part_h(conn,"data/movie_overview.csv")))
        print('\033[32m' + "Count h.ii: " + '\033[m' + str(db.part_hi(conn)))
        print('\033[32m' + "Count h.iii: " + '\033[m' + str(db.part_hii(conn)))
    except:
        print("Error in part h")

    conn.close()
    #################################################################################
    #################################################################################
  
