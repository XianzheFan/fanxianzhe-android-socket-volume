import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.awt.*;
import java.awt.event.KeyEvent;
 
public class Server {
   private static Robot robot = null;

   public static void main(String[] args) {
      
      try {
            robot = new Robot();
      } catch (AWTException e) {
         e.printStackTrace();
      }

      try {
         
         
         ServerSocket ss = new ServerSocket(8888);
         System.out.println("启动服务器....");
         Socket s = ss.accept();
         System.out.println("客户端:"+s.getInetAddress().getLocalHost()+"已连接到服务器");

         while (true){
            BufferedReader br = new BufferedReader(new InputStreamReader(s.getInputStream()));
            //读取客户端发送来的消息
            String mess = br.readLine();
            
            System.out.println("client message:"+mess);

            if (mess.contains("7,70")) {
               // volume down
               System.out.println("F");
               robot.keyPress(KeyEvent.VK_A);
            }

            

            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(s.getOutputStream()));
            bw.write("pop\n");
            bw.flush();
         }
         
      } catch (IOException e) {
         e.printStackTrace();
      }
   }
   
}