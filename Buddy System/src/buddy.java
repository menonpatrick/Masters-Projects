import java.util.*;
public class buddy {
	public static int size; // total available size of the memory
	public static int temp; // temporary variable which stores the actual available size of the memory
	public static int length; // used to identify the perfect slab of memory for the particular amount of memory entered by the user for either allocation or deallocation
	static int counter = 1; // used to indicate the number of processes
	static Scanner s = new Scanner(System.in); // Scanner function
	
	// case1 function; the allocation function
	public static void case1() {
		System.out.println("Enter the amount"); // accepting the amount of memory to be allocated
		int amt = s.nextInt(); // user input
		//temp = size;
		while(length >= amt) { // loop till the length is greater than or equal to the amount of memory entered by the user
			if((length/2) > amt) // if length divided by 2 is greater than the amount of memory entered by the user then proceed
				length = length/2; // divide length by 2
			else
				break; // if length divided by 2 is not greater than the amount of memory entered by the user then stop and break the loop
		} // while ends
		size = size - length; // reducing the available memory with the appropriate slab
		System.out.println("Process "+counter+" has been allocated a memory of size "+length+"K");
		counter++; // incrementing the counter to indicate the process number
		System.out.println("Total Memory remaining : " + size); // displaying the size of memory after the allocation of the memory entered by the user
		length = temp; // initializing length to the original size of memory
	} // case 1 ends
	
	// case2 function; the deallocation function
	public static void case2() {
		System.out.println("Enter the amount"); // accepting the amount of memory to be deallocated
		int amt = s.nextInt(); // user input
		while(length >= amt) { // loop till the length is greater than or equal to the amount of memory entered by the user
			if((length/2) > amt) // if length divided by 2 is greater than the amount of memory entered by the user then proceed
				length = length/2; // divide length by 2
			else
				break; // if length divided by 2 is not greater than the amount of memory entered by the user then stop and break the loop
		} // while ends
		// length finds out the exact slab of memory for the amount of memory entered by the user; then that particular slab is added to the available memory
		size = size + length; // increasing the available memory with the appropriate slab
		System.out.println("Process Deallocated and has released the memory of size "+length+"K");
		System.out.println("Total Memory remaining : " + size); // displaying the size of memory after the deallocation of the memory entered by the user
		length = temp; // initializing length to the original size of memory
	} // case 2 ends
	
	//********************Main Function***********************

	public static void main(String[] args) {
		
		System.out.println("Enter the total size of the Memory :");
		size = s.nextInt(); // accepting the total available memory
		temp = size; // saving the total memory size in a temporary variable
		length = size; // initializing variable length as same as the total size
		int ch = 0; // switching variable for switch case
		//int counter1 = 1;
		
		do {
			System.out.println("Enter your choice ::"); // user input
			System.out.println("1. Allocate"); // case 1
			System.out.println("2. Deallocate"); // case 2
			System.out.println("3. Exit"); // exit
			ch = s.nextInt(); // accepting the choice of user into "ch" variable
			// switch case to allow user to either allocate or deallocate the memory
			switch(ch) {
			case 1:
				case1(); // call case1 function
				break;
				
			case 2:
				case2(); // call case2 function
				break;
				
			case 3:
				System.exit(0); // exit
				break;
				
			default:
				System.out.println("Invalid Input");
			} // switch ends
		} // do ends
		
		while(ch!=3);
		
	} // main function ends
} // class ends
