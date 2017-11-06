import java.io.File;
import java.io.IOException;
import java.util.*;

public class simulation {
    
        public static Node head = null; // creating a pointer head
        public static int buses; // total number of buses will be stored
        public static int bss; // total number of bus stops will be stored
        public static int[] queue; // creating an array which will act as a queue at all 15 stops
        public static double timer = 0; // indicates the time taken by each event in seconds
        //static int type = 99;  // event identifier  || 0 = person || 1 = arrival || 2 = boarder ||
        public static double pmir; // Person's mean inter-arrival rate
        public static int dt; // Drive Time
        public static int bt; // Boarding Time
        
        public class Node { // class Node for initialization
            int type;
            double timer;
            int bus_stop;
            int bus_no;
            Node next;
            Node prev;

            public Node (int type, double timer, int bus_no, int bus_stop) { // constructor of class Node
                this.type = type; // type of event
                this.timer = timer; // time to capture the event time
                this.bus_no = bus_no; // No of bus
                this.bus_stop = bus_stop; // Bus stops
                this.next = null; // next pointer
                this.prev = null; // previous pointer
            } // node constructor ends
        } // class node ends
        
        
        // function for generating 15 person events || type = 0
        public void init(int type, double timer, int bus_no, int bus_stop) {
            // logic for inducing 15 person events into the LL
                    //this.type = type;
                    //this.timer = timer;
                    //this.bus_no = bus_no;
                    //this.bus_stop = bus_stop;
                
                    // logic for appending node
                    Node temp = new Node(type, timer, bus_no, bus_stop);
                
                    if(head == null) {  // Checking if the linked list is empty
                        temp.next = head;
                        temp.prev = null;
                        head = temp;
                    } // if ends
                    
                    else { // if the linked list is not empty
                        Node last = head;
                        while (last.next != null) // traversing till the last node
                            last = last.next;
                        
                     // appending the node and adjusting the pointers
                        temp.prev = last;
                        temp.next = null;
                        last.next = temp;
                    } // else ends
                    //queue[bus_stop] += 1;
                    System.out.println("Person Event Created at Bus Stop : "+temp.bus_stop);
        } // function init ends
        
        
        
        // function for generating 5 arrival events || type = 1
        public void init2(int type, double timer, int bus_no, int bus_stop) {
            // logic for inducing 5 arrival events into the LL
                    //this.type = type;
                    //this.timer = timer;
                    //this.bus_no = bus_no;
                    //this.bus_stop = bus_stop;
            
                    // logic for appending node
                    Node temp = new Node(type, timer, bus_no, bus_stop);
                            
                    if(head == null) {  // Checking if the linked list is empty
                        temp.next = head;
                        temp.prev = null;
                        head = temp;
                    } // if ends
                            
                    else { // if the linked list is not empty
                        Node last = head;
                        while (last.next != null) // traversing till the last node
                            last = last.next;
                        
                        // appending the node and adjusting the pointers
                        temp.prev = last;
                        temp.next = null;
                        last.next = temp;
                                
                    } // else ends
                    System.out.println("Arrival Event::");
                    System.out.print("Bus no "+bus_no);
                    System.out.println(" Present At bus stop : "+temp.bus_stop);
        } // function init2 ends
        
 
        
        // person function which is called from switch case
        public void person(double timer, int bus_stop) {
            double r = Math.random(); // calling random function
            //System.out.println("Random no :"+r);
            simulation.timer = timer + (pmir*r); // Mean arrival rate of a person at stop is 1 person/12 seconds
            int bs = bus_stop % (bss+1);  // Indicates the stop number where the person was generated
            System.out.println("At Bus Stop : "+bs+"\n");
            if(queue[bs] < 10) { // limit of the queue
                queue[bs] = queue[bs] + 1; // increments the value of queue for that bus stop
                generate_event(0,simulation.timer,0,bs); // generates another person event with updated values
            } // if ends
        } // person function ends
        
        
        
        // arrival function which is called from switch case
        public void arrival(double timer, int bus_no, int bus_stop) {
            //this.bus_no = bus_no; // indicates the bus no
            int bs = bus_stop % (bss+1); // indicates where the bus has arrived
            System.out.println("At Bus Stop : "+bs+" "+bss);
            if(queue[bs] != 0) { // if the queue is not null, proceed
                System.out.println("Queue is not Empty, generating the Boarder event");
                generate_event(2,simulation.timer,bus_no,bs); //generating boarder event at clock
                //queue[bs] = 0; // emptying the queue for that bus stop
                System.out.println("Person boarding the bus");
            } // if ends
            else {
                    System.out.println("Queue is empty, generating the Arrival event at Next Stop");
                    System.out.println("Bus proceeds to next stop"); 
                    simulation.timer = timer + dt; // 5 minutes drive time
                    generate_event(1,simulation.timer,bus_no,bs+1); // generates another arrival event with updated values at next stop
            } // else
        } // arrival function ends
        
        
     // boarder function which is called from switch case
        public void boarder(double timer, int bus_stop) {
            int bs = bus_stop % (bss+1);
            
            if(queue[bs] != 0) {
                //while (queue[bs] != 0) {
                System.out.println("Queue is not Empty, generating the Boarder event");
                simulation.timer = timer + bt; // 3 sec for a person to board
                queue[bs] = queue[bs] - 1; // decrements the value of queue for that bus stop
                generate_event(2,simulation.timer,0,bs); // generates boarder event with boarding time
                //} // while ends
            } // if ends
            
            else {
                bs++; // incrementing bus stop so the arrival function is called at next bus stop
                System.out.println("**Queue is empty, generating the arrival event at next stop**");
                generate_event(1,simulation.timer,0,bs); // generates arrival event
            } // else ends
        } // boarder function ends
        
        
        // generate an event i.e. append a new event in the link list with updated values
        public void generate_event(int type, double timer, int bus_no, int bus_stop ) {
            //this.type = type;
            //this.timer = timer;
            //this.bus_no = bus_no;
            //this.bus_stop = bus_stop;
            
            Node temp = new Node(type, timer, bus_no, bus_stop);
                    
            if(head == null) {  // Checking if the linked list is empty
                temp.next = head;
                temp.prev = null;
                head = temp;
            } // if ends
                    
            else { // if the linked list is not empty
                Node last = head;
                while (last.next != null)
                    last = last.next;
                
                // appending the node and adjusting the pointers
                temp.prev = last;
                temp.next = null;
                last.next = temp;
            } // else ends
        } // function to generate an event based on the 
        
        
        // Display function that displays the type of event from the LL
        public void display() {
            if(head == null) {  // Checking if no nodes are present
                System.out.println("No Nodes are present to display");
            } // if ends
            
            else { // if events already exists
                Node last = head;
                while(last.next != null) {
                    System.out.println(last.type);
                    last = last.next;
                } // while ends
                System.out.println(last.type); // printing the type of the event
            } // else ends
        } // display function ends
        
        
        
        // *********************************Main function begins*********************************
        public static void main(String zz[]) throws IOException {
            
            simulation s = new simulation();  // object creation
            
            // Reading a text file
            System.out.println(new File(".").getAbsoluteFile());
            File filePath = new File("./src/file.txt");
            Scanner scr = new Scanner(filePath); 
            List<Integer> integers = new ArrayList<>();
            while (scr.hasNext()) { // read the next token from the file
                if (scr.hasNextInt()) { // if the next token in the file is an integer
                    integers.add(scr.nextInt());
                } else { // if the next token in the file is not an integer, skip
                    scr.next();
                }
            }
            bss = integers.get(0);              // Reading no. of bus stops from file
            buses = integers.get(1);            // Reading no. of buses from file
            dt = integers.get(2);               // Reading drive time of buses between 2 bus stops from file
            int pmar = integers.get(3);         // Reading person's mean arrival rate from file
            bt = integers.get(4);               // Reading boarding time from file
            double st = integers.get(5);        // Reading total simulation time from file
            
            System.out.println("Bus stops: "+bss);
            System.out.println("Buses: "+buses);
            System.out.println("Drive Time: "+dt+" mins");
            System.out.println("Mean arrival rate: "+pmar+" person/min");
            System.out.println("Boarding Time: "+bt+" sec");
            System.out.println("Stop Time: "+st+" hour(s)");
            
            dt = dt * 60;					// Converting into minutes
            pmir = 60.0/pmar;               // Person's Mean inter-arrival rate 
            st = st * 3600; 
            queue = new int[bss+1];
            
            int ch;  // switch variable
            int j = 1; // bus stop for arrival event
            int k = 1; // bus stop for person event
            int b = 1; // bus number for arrival event
            
            // Considering there is at least one person at every bus stop
            System.out.println("\nThe Linked List is empty and Initialization Begins");
            System.out.println(bss+" person events and "+buses+" arrival events are stored\n");
            
            // Initializing the Linked List
            for(int i=1;i<= buses+bss;i++) {
                if (i % (bss/buses+1) == 1) {
                    s.init2(1,0,b,j); // method calling
                    j = (j+bss/buses) % (bss+1); // adjusting the arrival event at equidistant
                    b++;
                } // if ends
                else {
                    s.init(0,0,0,k); // method calling
                    k++; // bus stop value
                } // else ends
            } // for ends
            System.out.println("\nInitialization of the LL is done\n");
            
            
            //System.out.println("Head type"+head.type);
            Node last = head;
            System.out.println("Timer before traversing the LL: "+timer);
            while(last.next != null && timer < st) { // simulation works until timer hits 1 hour
                ch = last.type;

                    switch(ch) {
                    case 0:
                        System.out.println("Person Case");
                        s.person(timer, last.bus_stop);
                        //System.out.println("Timer - "+simulation.timer);
                        break;
                        
                    case 1:
                        System.out.println("Arrival Case");
                        s.arrival(timer, last.bus_no, last.bus_stop);
                        //System.out.println("Bus Stop"+last.bus_stop);
                        break;
                        
                    case 2:
                        System.out.println("Boarder Case");
                        s.boarder(timer, last.bus_stop);
                        break;
                    } // switch ends
                last = last.next;
            } // while ends
            
            // for considering the last node present in the LL
            ch = last.type;
                switch(ch) {
                case 0:
                    System.out.println("Person Case");
                    s.person(timer, last.bus_stop);
                    break;
                    
                case 1:
                    System.out.println("Arrival Case");
                    s.arrival(timer, last.bus_no, last.bus_stop);
                    //System.out.println("Bus Stop"+last.bus_stop);
                    break;
                    
                case 2:
                    System.out.println("Boarder Case");
                    s.boarder(timer, last.bus_stop);
                    break;
                } // switch ends
                
                
            // displaying the final record in the Linked List
            s.display();
            scr.close();
        } // main ends
} // class bus simulation ends