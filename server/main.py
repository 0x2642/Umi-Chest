#-*- coding: UTF-8 -*-
import  socketserver,classes.UmiChestServer

if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer(("127.0.0.1",12345),classes.UmiChestServer.UmiChestServer)
    server.serve_forever()
