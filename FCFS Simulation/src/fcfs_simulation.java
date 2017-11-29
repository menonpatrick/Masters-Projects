import java.util.Random;
public class fcfs_simulation {
		public static int process_id [] = new int [11]; // indicates the process number
		public static double arrival_time [] = new double [11]; // indicates the arrival time of the respective processes
		public static double burst_time [] = new double [11]; //indicates the burst time of the respective processes
		public static double trt [] = new double [11]; // indicates the turnaround time of the respective processes
		public static double wt [] = new double [11];  // indicates the waiting time of the respective processes
		public static double ct [] = new double [11];  // indicates the completion time of the respective processes
		public static double io [] = new double [11];  // indicates the io time of the respective processes
		public static int[] pcb = new int [11]; // array of pcb for storing the entries of the processes
		public static int[] ready_queue = new int [11]; // indicates the ready queue
		public static int[] io_queue = new int [11]; // indicates the I/O queue
		public static int cpu_state = 0; // indicates the state of the cpu; || 0 = free || 1 = busy  ||
		public static int pcb_state = 0; // indicates the state of the pcb; || 0 = idle || 1 = running  ||
		public static double io_new = 30; // indicates the initial time required by the process for I/O
		
		// arrival function
		// as soon as the process is created/ generated, the arrival function for that process is called
		public static void arrival(int p, double a, double b) {
			double avg1 = 0; // avg variable declared to find the average of turnaround time
			double avg2 = 0; // avg variable declared to find the average of waiting time
			int k = 0; // variable for managing the pcb entry
			pcb[k] = p; // creating a PCB entry into the pcb array
			System.out.println("PCB entry created for Process "+p);
			// checking if the state of cpu is free
			if(cpu_state == 0) { // proceeds only if the state of the cpu is free
				System.out.println("** CPU is free **"); // indicating that the cpu is free
				cpu_state = 1; // making the state of cpu from idle to busy
				pcb_state = 1; // making the pcb state from idle to running
				System.out.println("** CPU is Busy Processing Process "+p+" **");
				// calculating completion time and turnaround time
				for(int i=1;i<=10;i++) {
					ct[i] = ct[i-1] + burst_time[i]; // completion time calculated by considering the completion time of the previous process and the burst time of the current process
					trt[i] = ct[i] - arrival_time[i]; // turnaround time calculated by considering the completion time of the current process and the arrival time of the current process
				} // for ends
				
				// calculating average turnaround time
				//double avg = 0;
				for(int u=1;u<=10;u++) {
					avg1 = avg1 + trt[u]; // calculating the average time of of the turnaround time
					avg2 = avg2 + wt[u]; // calculating the average time of of the waiting time
				} // for ends
				avg1 = avg1/10;
				avg2 = avg2/10;
				//System.out.println("Average Turnaround Time : "+avg);
				
				// calculating waiting time
				wt[p] = trt[p] - burst_time[p]; // waiting time is equal to turnaround time minus burst time
				k++; // index for pcb array incremented
			} // if cpu_state ends
			// if the state of cpu is not free
			else {
				System.out.println("** CPU is NOT free **"); // indicating that the cpu is not free
				pcb_state = 0; // pcb state changed to ready
				ready_queue[p] = p; // updating ready queue
			}// else ends
			io_interrupt(process_id[p]);
			completion(process_id[p]); // calling completion function
			if(p == 10) {
				System.out.println("Average Turnaround Time : "+avg1);
				System.out.println("Average Waiting Time : "+avg2);
		} // if ends
		} // arrival function ends
	
		// completion function
		public static void completion(int p) {
			for(int x=1;x<=10;x++)
				if(pcb[x] == p) { // searching for the pcb entry
					pcb[x] = 0; // pcb entry destroyed
					//System.out.println("PCB entry destroyed for Process "+p); 
				} // if ends
			System.out.println("PCB entry destroyed for Process "+p); 
			System.out.println("Process execution completed");
			System.out.println("** CPU is made free **");
			cpu_state = 0; // making the cpu state from busy to idle
			pcb_state = 0; // making the pcb state from running to idle
			if(ready_queue[1] != 0) { // checking if the ready queue is not empty
				completion(process_id[1]); // calling completion function for the process which is currently ready
				pcb_state = 1; // indicates that the pcb state is running
			} // if ends
			else { // if the ready queue is empty
				cpu_state = 0; // making the state of cpu as free
			} // else ends
		} // completion function ends
		
		// I/O function where the process enters into the I/O queue after the specified amount of time
		public static void io_interrupt(int p) {
			System.out.println("Process "+p+" enters the I/O queue after "+io_new+"ms");
			System.out.println("Process "+p+" stays for +60ms");
			System.out.println("The total execution time for the process "+p+" becomes "+io_new+" + 60");
			io_new = io_new+5;
		} // io_interrupt ends
		
		// display1 function
		// displays the arrival time and the burst time
		public static void display1() {
			System.out.println("Initial Information -->");
			System.out.println("Process \t Arrival Time \t Burst Time");
			for(int i=1;i<=10;i++)
				System.out.println(process_id[i]+"\t\t\t"+arrival_time[i]+"\t\t"+burst_time[i]);
			System.out.println();
			System.out.println();
		} // display1 function ends

		// display2 function
		// displays the waiting time and the turnaround time
		public static void display2() {
			System.out.println("Your Information is as follows -->");
			System.out.println("Process \t Waiting Time \t Turnaround Time");
			for(int i=1;i<=10;i++)
				System.out.println(process_id[i]+"\t\t\t"+wt[i]+"\t\t"+trt[i]);
			System.out.println();
			System.out.println();
			for(int i=1;i<=10;i++) {
				System.out.println();
				System.out.println("Process "+process_id[i]+" arrived at "+arrival_time[i]+" & completed at "+ct[i]);
			} // for ends
		} // display2 function ends
		
		// display the processes in the form of a gantt chart
		public static void display3() {
			System.out.println();
			System.out.println("Gantt Chart:");
			for(int i=1;i<=10;i++) {
				System.out.print("|\tP"+process_id[i]);
			} // for ends
			System.out.print("|");
			System.out.println();
			for(int i=0;i<=10;i++) {
				System.out.print(ct[i]+" \t");
			} // for ends
			double throughput = 10/ct[10];
			System.out.println();
			System.out.println();
			System.out.println("Throughput = "+throughput);
			// considering the context switching time as 15 ms for all the processes; i.e. the time required for context switching all the processes is 15ms
			double cpu_utilization = (ct[10]/(ct[10]+15))*100;
			System.out.println("Cpu Utilization :"+cpu_utilization+"%");
		} // display3 function ends
	
		// *************************Main Function Begins*************************
		public static void main (String z[]) {
			int min = 1; // minimum value used for generating random values of burst time
			int max = 4; // maximum value used for generating random values of burst time
			int io_initial = 30; // used to store the I/O time for all the processes
			System.out.println("First Come First Serve (Simulation) :");
			System.out.println();
			Random random = new Random(); // creating an object of random function
			int i; // used for iterating the last for loop
			// storing the values of the processes
			for(int h=1;h<=10;h++)
				process_id [h] = h; // setting up the process number for each of the 10 processes
			// storing the arrival time of the processes
			for(int h=1;h<=10;h++)
				arrival_time [h] = 0; // assuming that all the processes have arrived at the same time
			// storing the burst time of the processes
			for(int h=1;h<=10;h++)
				burst_time [h] = (random.nextInt(max-min)+1)+min; // generating random burst time for all the processes between 2 and 4
			// storing the inter I/O time
			for(int h=1;h<=10;h++) {
				io [h] = io_initial;
				io_initial = io_initial+5;
			} // for ends	
			for(i=1;i<=10;i++) {
				arrival(process_id[i],arrival_time[i],burst_time[i]);
				//completion(process_id[i]);
			} // for ends
			display1(); // display1 function called
			display2(); // display2 function called
			display3(); // display3 function called
		} // main method ends
} // class ends