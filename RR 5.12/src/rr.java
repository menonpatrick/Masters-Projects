
public class rr {
		public static int process_id [] = new int [6]; // indicates the process number
		public static int process_id_copy [] = new int [6];
		public static double arrival_time [] = new double [6]; // indicates the arrival time of the respective processes
		public static double priority [] = new double [6]; // indicates the priority of the processes
		public static double burst_time [] = new double [6]; // indicates the burst time of the respective processes
		public static double burst_time_copy [] = new double [6];
		public static double trt [] = new double [6]; // indicates the turnaround time of the respective processes
		public static double wt [] = new double [6];  // indicates the waiting time of the respective processes
		public static double ct [] = new double [6];  // indicates the completion time of the respective processes
		public static int[] pcb = new int [6]; // array of pcb for storing the entries of the processes
		public static int[] ready_queue = new int [6]; // indicates the ready queue
		public static int cpu_state = 0; // indicates the state of the cpu; || 0 = free || 1 = busy  ||
		public static int pcb_state = 0; // indicates the state of the pcb; || 0 = idle || 1 = running  ||
		public static int count = 1; // counter initialized
		public static int quantum = 1; // initializing the value of quantum
		public static int d = 1; // used to loop the processes array
		public static int round1 [] = new int [51]; // used to store process number
		public static int round2 [] = new int [51]; // used to store the burst time; i.e. the quantum
		
		// arrival function
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
					else
						 if(round1[i]!=0)
							 ct[5] = round2[i];
				} // for ends
				for(int i=1;i<=5;i++) {
					//System.out.println(ct[i-1]+"+"+burst_time[i]);
					//System.out.println("Completion Time of process :"+i+" is"+ct[i]);
					trt[i] = ct[i] - arrival_time[i];
				} // for ends
				
				// calculating average turnaround time
				for(int u=1;u<=5;u++) {
					avg1 = avg1 + trt[u];
					avg2 = avg2 + wt[u];
				} // for ends
				avg1 = avg1/5;
				avg2 = avg2/5;
				//System.out.println("Average Turnaround Time : "+avg);
				
				// calculating waiting time
				wt[p] = trt[p] - burst_time[p];
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
			completion(process_id[p]); // calling completion function
		} // arrival function ends
	
		// completion function
			public static void completion(int p) {
				for(int x=1;x<=5;x++)
					if(pcb[x] == p) // searching for the pcb entry
						pcb[x] = 0; // pcb entry destroyed
				System.out.println("PCB entry destroyed for Process "+p); 
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
	
		
		// display1 function
		// displays the arrival time and the burst time
		public static void display1() {
			System.out.println("Initial Information -->");
			System.out.println("Process \t Arrival Time \t Burst Time \t    Priority");
			for(int i=1;i<=5;i++)
				System.out.println(process_id[i]+"\t\t\t"+arrival_time[i]+"\t\t"+burst_time_copy[i]+"\t\t"+priority[i]);
			System.out.println();
			System.out.println();
		} // display1 function ends
	
		public static void temp_sort() {
			double temp; // temporary variable
			int temp1; // temporary variable
			for(int i=1;i<5;i++) {
				for(int j=i+1;j<=5;j++) {
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
			for(int r=1;r<=5;r++) {
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
				} // display3 function ends
		
		// sorting the processes according to the priority
		public static void sort() {
			double temp; // temporary variable
			int temp1; // temporary variable
			for(int i=1;i<5;i++) {
				for(int j=i+1;j<=5;j++) {
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
		
		// managing the processes based on the burst time and the time quantum
		public static void manage() {
			int bubble = 1;
			for(int w=1;w<=50;w++) {
				if(process_id_copy[d] != 0) { // proceeds only if the value of the process id is not 0
					round1 [w] = process_id_copy[d]; // save the process id into the round1 array
					round2 [w] = bubble; // saving the completion time into round2 array; the execution time here is same since the time quantum is 1
					burst_time[d] = burst_time[d]-quantum; // reducing the burst time of that particular process by the specified time quantum
					bubble++;
				} // if ends
				if(burst_time[d] == 0) // if the burst time of that particular process reaches 0; the process completes its scheduling
					process_id_copy[d] = 0;
				d++; // incrementing the value of d which is related to the looping of the process id array
				if(d>5)
					d=d%5;
			} // for ends
		} // manage function ends
		
		public static void main (String z[]) {
			System.out.println("Round Robin (5.12) :");
			System.out.println();
			int i;
			// storing the values of the processes
			process_id [1] = process_id_copy [1] = 1; // process 1
			process_id [2] = process_id_copy [2] = 2; // process 2
			process_id [3] = process_id_copy [3] = 3; // process 3
			process_id [4] = process_id_copy [4] = 4; // process 4
			process_id [5] = process_id_copy [5] = 5; // process 5
			// storing the priority of the processes
			priority [1] = 3; // priority of process 1
			priority [2] = 1; // priority of process 2
			priority [3] = 3; // priority of process 3
			priority [4] = 4; // priority of process 4
			priority [5] = 2; // priority of process 5
			// storing the burst time of the processes
			burst_time [1] = burst_time_copy[1] = 10; // burst time of process 1
			burst_time [2] = burst_time_copy[2] = 1; // burst time of process 2
			burst_time [3] = burst_time_copy[3] = 2; // burst time of process 3
			burst_time [4] = burst_time_copy[4] = 1; // burst time of process 4
			burst_time [5] = burst_time_copy[5] = 5; // burst time of process 5
			// storing the arrival time of the processes
			for(i=1;i<=5;i++)
				arrival_time[i] = 0; // making every element of array as 0
			sort(); // sorting function called
			manage(); // managing the processes based on the burst time
			for(i=1;i<=5;i++) {
				arrival(process_id[i],arrival_time[i],burst_time[i]); // calling arrival function
				//completion(process_id[i]); // calling completion function
			} // for ends
			temp_sort(); // function call
			/*
			for(int t=1;t<=5;t++)
				System.out.println("Completion time of"+t+" is "+ct[t]);
			*/
			display1(); // display1 function called
			display2(); // display2 function called
			display3(); // display3 function called
		} // main method ends
} // class ends