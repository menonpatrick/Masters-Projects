
public class fcfs {
		public static int process_id [] = new int [4]; // indicates the process number
		public static double arrival_time [] = new double [4]; // indicates the arrival time of the respective processes
		public static double burst_time [] = new double [4]; //indicates the burst time of the respective processes
		public static double trt [] = new double [4]; // indicates the turnaround time of the respective processes
		public static double wt [] = new double [4];  // indicates the waiting time of the respective processes
		public static double ct [] = new double [4];  // indicates the completion time of the respective processes
		public static int[] pcb = new int [4]; // array of pcb for storing the entries of the processes
		public static int[] ready_queue = new int [4]; // indicates the ready queue
		public static int cpu_state = 0; // indicates the state of the cpu; || 0 = free || 1 = busy  ||
		public static int pcb_state = 0; // indicates the state of the pcb; || 0 = idle || 1 = running  ||
	
		// arrival function
		public static void arrival(int p, double a, double b) {
			double avg = 0; // avg variable declared to find the average of turnaround time
			int k = 0; // variable for managing the pcb entry
			pcb[k] = p; // creating a PCB entry into the pcb array
			System.out.println("PCB entry created for Process "+p);
			// checking if the state of cpu is free
			if(cpu_state == 0) {
				System.out.println("** CPU is free **"); // indicating that the cpu is free
				cpu_state = 1; // making the state of cpu from idle to busy
				pcb_state = 1; // making the pcb state from idle to running 
				// calculating completion time and turnaround time
				for(int i=1;i<=3;i++) {
					ct[i] = ct[i-1] + burst_time[i];
					trt[i] = ct[i] - arrival_time[i];
				} // for ends
				
				// calculating average turnaround time
				//double avg = 0;
				for(int u=1;u<=3;u++) {
					avg = avg + trt[u];
				} // for ends
				avg = avg/3;
				//System.out.println("Average Turnaround Time : "+avg);
				
				// calculating waiting time
				wt[p] = trt[p] - burst_time[p];
				k++;
			} // if cpu_state ends
			// if the state of cpu is not free
			else {
				System.out.println("** CPU is NOT free **"); // indicating that the cpu is not free
				pcb_state = 0; // pcb state changed to ready
				ready_queue[p] = p; // updating ready queue
			}// else ends
			completion(process_id[p]); // completion function call
			if(p == 3)
				System.out.println("Average Turnaround Time : "+avg);
		} // arrival function ends
	
		// completion function
		public static void completion(int p) {
			for(int x=1;x<=3;x++)
				if(pcb[x] == p) // searching for the pcb entry
					pcb[x] = 0; // pcb entry destroyed
			System.out.println("PCB entry destroyed for Process "+p); 
			System.out.println("** CPU is made free **"); 
			cpu_state = 0; // making the cpu state from busy to idle
			pcb_state = 0; // making the pcb state from running to idle
			for(int x=1;x<=3;x++) {
				if(ready_queue[1] != 0) { // checking if the ready queue is not empty
					completion(process_id[1]); // calling completion function
					pcb_state = 1; // indicates that the pcb state is running
				} // if ends
				else { // if the ready queue is empty
					cpu_state = 0; // making the state of cpu as free
				} // else ends
			} // for ends
		} // completion function ends
	
		// display1 function
		// displays the arrival time and the burst time
		public static void display1() {
			System.out.println("Initial Information -->");
			System.out.println("Process \t Arrival Time \t Burst Time");
			for(int i=1;i<=3;i++)
				System.out.println(process_id[i]+"\t\t\t"+arrival_time[i]+"\t\t"+burst_time[i]);
			System.out.println();
			System.out.println();
		} // display1 function ends
	
		// display2 function
		// displays the waiting time and the turnaround time
		public static void display2() {
			System.out.println("Your Information is as follows -->");
			System.out.println("Process \t Waiting Time \t Turnaround Time");
			for(int i=1;i<=3;i++)
				System.out.println(process_id[i]+"\t\t\t"+wt[i]+"\t\t"+trt[i]);
			System.out.println();
			System.out.println();
			for(int i=1;i<=3;i++) {
				System.out.println();
				System.out.println("Process "+process_id[i]+" arrived at "+arrival_time[i]+" & completed at "+ct[i]);
			} // for ends
		} // display2 function ends
		
		// display the processes in the form of a gantt chart
		public static void display3() {
			System.out.println();
			System.out.println("Gantt Chart:");
			for(int i=1;i<=3;i++) {
				System.out.print("|\tP" +process_id[i]);
			} // for ends
			System.out.print("|");
			System.out.println();
			for(int i=0;i<=3;i++) {
				System.out.print(ct[i]+" \t");
			} // for ends
		} // display3 function ends
		
		public static void main (String z[]) {
			System.out.println("First Come First Serve (5.3):");
			System.out.println();
			int i;
			// storing the values of the processes
			process_id [1] = 1; // process 1
			process_id [2] = 2; // process 2
			process_id [3] = 3; // process 3
			// storing the arrival time of the processes
			arrival_time [1] = 0.0; // arrival time of process 1
			arrival_time [2] = 0.4; // arrival time of process 2
			arrival_time [3] = 1.0; // arrival time of process 3
			// storing the burst time of the processes
			burst_time [1] = 8; // burst time of process 1
			burst_time [2] = 4; // burst time of process 2
			burst_time [3] = 1; // burst time of process 3
			
			for(i=1;i<=3;i++) {
				arrival(process_id[i],arrival_time[i],burst_time[i]); // arrival function call
				//completion(process_id[i],arrival_time[i],burst_time[i]); // completion fumction call
			} // for ends
			display1(); // display1 function called
			display2(); // display2 function called
			display3(); // display3 function called
		
		} // main method ends
} // class ends