import java.util.Random;
public class rr_simulation {
		public static int process_id [] = new int [11]; // indicates the process number
		public static int process_id_copy [] = new int [11];
		public static double arrival_time [] = new double [11]; // indicates the arrival time of the respective processes
		public static double priority [] = new double [11]; // indicates the priority of the processes
		public static double burst_time [] = new double [11]; // indicates the burst time of the respective processes
		public static double burst_time_copy [] = new double [11];
		public static double trt [] = new double [11]; // indicates the turnaround time of the respective processes
		public static double wt [] = new double [11];  // indicates the waiting time of the respective processes
		public static double ct [] = new double [11];  // indicates the completion time of the respective processes
		public static double io [] = new double [11];  // indicates the io time of the respective processes
		public static int[] pcb = new int [11]; // array of pcb for storing the entries of the processes
		public static int[] ready_queue = new int [11]; // indicates the ready queue
		public static int cpu_state = 0; // indicates the state of the cpu; || 0 = free || 1 = busy  ||
		public static int pcb_state = 0; // indicates the state of the pcb; || 0 = idle || 1 = running  ||
		public static int count = 1; // counter initialized
		public static int quantum = 1; // initializing the value of quantum
		public static int d = 1; // used to loop the processes array
		public static double round1 [] = new double [51]; // used to store process number
		public static double round2 [] = new double [51]; // used to store the burst time; i.e. the quantum
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
			if(cpu_state == 0) {
				System.out.println("** CPU is free **"); // indicating that the cpu is free
				cpu_state = 1; // making the state of cpu from idle to busy
				pcb_state = 1; // making the pcb state from idle to running
				System.out.println("** CPU is Busy Processing Process "+p+" **");
				// calculating completion time and turnaround time
				for(int i=1;i<=50;i++) {
					if(round1[i] == 1 && round1[i]!=0)
						ct[1] = round2[i];
					else if(round1[i] == 2 && round1[i]!=0)
						ct[2] = round2[i];
					else if(round1[i] == 3 && round1[i]!=0)
						ct[3] = round2[i];
					else if(round1[i] == 4 && round1[i]!=0)
						ct[4] = round2[i];
					else if(round1[i] == 5 && round1[i]!=0)
						ct[5] = round2[i];
					else if(round1[i] == 6 && round1[i]!=0)
						ct[6] = round2[i];
					else if(round1[i] == 7 && round1[i]!=0)
						ct[7] = round2[i];
					else if(round1[i] == 8 && round1[i]!=0)
						ct[8] = round2[i];
					else if(round1[i] == 9 && round1[i]!=0)
						ct[9] = round2[i];
					else
						 if(round1[i]!=0)
							 ct[10] = round2[i];
				} // for ends
				for(int i=1;i<=10;i++) {
					//System.out.println(ct[i-1]+"+"+burst_time[i]);
					//System.out.println("Completion Time of process :"+i+" is"+ct[i]);
					trt[i] = ct[i] - arrival_time[i];
				} // for ends
				
				// calculating average turnaround time
				for(int u=1;u<=10;u++) {
					avg1 = avg1 + trt[u];
					avg2 = avg2 + wt[u];
				} // for ends
				avg1 = avg1/10;
				avg2 = avg2/10;
				//System.out.println("Average Turnaround Time : "+avg);
				
				// calculating waiting time
				wt[p] = trt[p] - burst_time[p];
				k++; // index for pcb array incremented
			} // if ends
			// if the state of cpu is not free
			else {
				System.out.println("** CPU is NOT free **"); // indicating that the cpu is not free
				pcb_state = 0; // pcb state changed to ready
				ready_queue[p] = p; // updating ready queue
			}// else ends
			
			if(count == 5) {
				System.out.println("Average Turnaround Time : "+avg1);
				System.out.println("Average Waiting Time : "+avg2);
			} // if ends
			count++; // incrementing the counter
			//System.out.println(count);
			io_interrupt(process_id[p]);
			completion(process_id[p]);
		} // arrival function ends
	
		// completion function
		public static void completion(int p) {
			for(int x=1;x<=10;x++)
				if(pcb[x] == p) // searching for the pcb entry
					pcb[x] = 0; // pcb entry destroyed
			System.out.println("PCB entry destroyed for Process "+p);
			System.out.println("Process execution completed");
			System.out.println("** CPU is made free **");
			cpu_state = 0; // making the cpu state from busy to idle
			pcb_state = 0; // making the pcb state from running to idle
			if(ready_queue[1] != 0) { // checking if the ready queue is not empty
				completion(process_id[1]); // calling completion function
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
	/*
		public static void temp_sort() {
			double temp; // temporary variable
			int temp1; // temporary variable
			for(int i=1;i<10;i++) {
				for(int j=i+1;j<=10;j++) {
					if(priority[i]>=priority[j]) {
						// sorting the equivalent completion time & turnaround time array
						temp = ct[i];
						ct[i] = ct[j];
						ct[j] = temp;
						temp = trt[i];
						trt[i] = trt[j];
						trt[j] = temp;
					} // if ends
				} // j for ends
			} // i for ends
		} // sort function ends
		*/
		
		// display2 function
		// displays the waiting time and the turnaround time
		public static void display2() {
			System.out.println("Your Information is as follows -->");
			System.out.println("Process \t Completion Time");
			for(int i=1;i<=50;i++)
				if(round1[i]!=0)
					System.out.println(round1[i]+"\t \t \t"+round2[i]);
			System.out.println();
			System.out.println();
			//temp_sort();
			for(int r=1;r<=10;r++) {
				System.out.println();
				System.out.println("Process "+process_id[r]+" completed at "+ct[r]+" with a turnaround time of "+trt[r]);
			} // for ends
		} // display2 function ends
	
		// display the processes in the form of a gantt chart
		public static void display3() {
			round2[0]=0;
			System.out.println();
			System.out.println("Gantt Chart:");
			for(int i=1;i<=50;i++) {
				if(round1[i]!=0)
					System.out.print("|\tP" +round1[i]);
			} // for ends
			System.out.print("|");
			System.out.println();
			System.out.print(round2[0]+" \t ");
			for(int i=0;i<=50;i++) {
				if(round1[i]!=0) {
					System.out.print(round2[i]+" \t ");
				} // if ends
			} // for ends
			double throughput = 10/ct[10];
			System.out.println();
			System.out.println();
			System.out.println("Throughput = "+throughput);
			// considering the context switching time as 15 ms for all the processes; i.e. the time required for context switching all the processes is 15ms
			double cpu_utilization = (ct[10]/(ct[10]+15))*100;
			System.out.println("Cpu Utilization :"+cpu_utilization+"%");
		} // display3 function ends
		
		/*
		// sorting the processes according to the priority
		public static void sort() {
			double temp; // temporary variable
			int temp1; // temporary variable
			for(int i=1;i<10;i++) {
				for(int j=i+1;j<=10;j++) {
					if(priority[i]>=priority[j]) {
						// sorting the processes based on their burst time
						temp = burst_time[i];
						burst_time[i] = burst_time[j];
						burst_time[j] = temp;
						// sorting the equivalent process_id array
						temp1 = process_id[i];
						process_id[i] = process_id[j];
						process_id[j] = temp1;
						// sorting the equivalent priority array
						temp = priority[i];
						priority[i] = priority[j];
						priority[j] = temp;
						// sorting the equivalent completion time array
						temp = ct[i];
						ct[i] = ct[j];
						ct[j] = temp;
					} // if ends
					// considering the case where multiple processes have the same priority; in this case, FCFS is considered i.e. the processes that arrives first will get higher precedence
					if(priority[i]==priority[j] && process_id[i]>process_id[j]) {
						// sorting the processes based on their burst time
						temp = burst_time[i];
						burst_time[i] = burst_time[j];
						burst_time[j] = temp;
						// sorting the equivalent process_id array
						temp1 = process_id[i];
						process_id[i] = process_id[j];
						process_id[j] = temp1;
						temp1 = process_id_copy[i];
						process_id_copy[i] = process_id_copy[j];
						process_id_copy[j] = temp1;
						// sorting the equivalent priority array
						temp = priority[i];
						priority[i] = priority[j];
						priority[j] = temp;
					} // 2nd if ends
				} // j for ends
			} // i for ends
		} // sort function ends
		*/
		
		// managing the processes based on the burst time and the time quantum
		public static void manage() {
			int bubble = quantum; // indicates the completion time
			int count = 1;
			double temp[] = new double [11];
			for(int w=1;w<=50;w++) {
				if(process_id_copy[d] != 0) { // proceeds only if the value of the process id is not 0
					if(burst_time_copy[d]<quantum) {
						round1 [w] = process_id_copy[d]; // save the process id into the round1 array
						round2 [w] = temp[count-1]+burst_time_copy[d]; // saving the completion time into round2 array; the execution time here is same since the time quantum is 1
						temp[count] = round2[w];
						burst_time_copy[d] = 0; // reducing the burst time of that particular process by the specified time quantum
						count++;
						if(count>10)
							count = 1;
					} // if ends
					else {
					round1 [w] = process_id_copy[d]; // save the process id into the round1 array
					round2 [w] = bubble; // saving the completion time into round2 array; the execution time here is same since the time quantum is 1
					temp[count] = round2[w];
					burst_time_copy[d] = burst_time_copy[d]-quantum; // reducing the burst time of that particular process by the specified time quantum
					bubble=bubble+quantum;
					count++;
					if(count>10)
						count = 1;
					} // else ends
				} // if ends
				if(burst_time_copy[d] == 0) // if the burst time of that particular process reaches 0; the process completes its scheduling
					process_id_copy[d] = 0; // the value for that process is marked as 0
				d++; // incrementing the value of d which is related to the looping of the process id array
				if(d>10)
					d=d%10;
			} // for ends
		} // manage function ends
		
		// *************************Main Function Begins*************************
		public static void main (String z[]) {
			int min = 1; // minimum value used for generating random values of burst time
			int max = 4; // maximum value used for generating random values of burst time
			int io_initial = 30; // used to store the I/O time for all the processes
			System.out.println("Round Robin Simulation :");
			System.out.println();
			Random random = new Random(); // creating an object of random function
			int i; // used for iterating the last for loop
			// storing the values of the processes
			for(int h=1;h<=10;h++)
				process_id [h] = process_id_copy [h] = h; // setting up the process number for each of the 10 processes
			// storing the burst time of the processes
			for(int h=1;h<=10;h++)
				burst_time[h] = burst_time_copy[h] = (random.nextInt(max-min)+1)+min; // generating random burst time for all the processes between 2 and 4
			// storing the arrival time of the processes
			for(int h=1;h<=10;h++)
				arrival_time[h] = 0; // making every element of array as 0
			// storing the inter I/O time
			for(int h=1;h<=10;h++) {
				io [h] = io_initial;
				io_initial = io_initial+5;
			} // for ends
			//sort(); // sorting function called
			manage(); // managing the processes based on the burst time
			for(i=1;i<=10;i++) {
				arrival(process_id[i],arrival_time[i],burst_time[i]); // calling arrival function
				//completion(process_id[i]); // calling completion function
			} // for ends
			//temp_sort(); // function call
			/*
			for(int t=1;t<=5;t++)
				System.out.println("Completion time of"+t+" is "+ct[t]);
			*/
			display1(); // display1 function called
			display2(); // display2 function called
			display3(); // display3 function called
		} // main method ends
} // class ends