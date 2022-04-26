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
         System.out.println("server....");
         Socket s = ss.accept();
         System.out.println("client:"+s.getInetAddress().getLocalHost()+"connected to the server");

         while (true){
            BufferedReader br = new BufferedReader(new InputStreamReader(s.getInputStream()));
            //
            String mess = br.readLine();
            
            System.out.println("client message:"+mess);

            if (mess.contains("7,70")) {
               // volume down
               System.out.println("F");
               robot.keyPress(KeyEvent.VK_F);
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