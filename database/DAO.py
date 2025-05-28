from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    @staticmethod
    def getAlbums(dMin):
        cnx=DBConnect.get_connection()
        cursor=cnx.cursor(dictionary=True)
        query="""select a.AlbumId,a.Title,a.ArtistId, sum(t.Milliseconds)/1000/60 as dTot
                from album a , track t
                where a.AlbumId =t.AlbumId 
                group by a.AlbumId 
                having dTot>%s """
        cursor.execute(query, (dMin,)) #dMin in minuti
        results=[]
        for row in cursor:
            results.append(Album(**row))

        return results

    @staticmethod
    def getAllEdges(idMapAlbum):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinctrow t1.AlbumId as a1, t2.AlbumId  as a2
    from track t1, track t2, playlisttrack p , playlisttrack p2 
    where t2.TrackId=p2.TrackId and t1.TrackId=p.TrackId and p2.PlaylistId =p.PlaylistId and t1.AlbumId<t2.AlbumId  """
        cursor.execute(query)  # dMin in minuti
        results = []
        for row in cursor:
            if row["a1"] in idMapAlbum and row["a2"] in idMapAlbum:
                results.append((idMapAlbum[row["a1"]], idMapAlbum[row["a2"]]))

        return results
