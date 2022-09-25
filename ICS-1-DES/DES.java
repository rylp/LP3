package des;

public class DES 
{
	//MEGA KHATARKANK
	//These matrices will be provided in the lab.
	public static final int P10[] = { 3, 5, 2, 7, 4, 10, 1, 9, 8, 6}; 
	public static final int P8[] = { 6, 3, 7, 4, 8, 5, 10, 9};
    public static final int P4[] = { 2, 4, 3, 1};
	
    public static final int IP[] = { 2, 6, 3, 1, 4, 8, 5, 7};
    public static final int IP_Inverse[] = { 4, 1, 3, 5, 7, 2, 8, 6};
    
    public static final int EP[] = { 4, 1, 2, 3, 2, 3, 4, 1};
    
    public static final int S0[][] = {{ 1, 0, 3, 2},{ 3, 2, 1, 0},{ 0, 2, 1, 3},{ 3, 1, 3, 2}};
    public static final int S1[][] = {{ 0, 1, 2, 3},{ 2, 0, 1, 3},{ 3, 0, 1, 2},{ 2, 1, 0, 3}};
	
	public static int K1[];
	public static int K2[];
	
	//Function to print the array
	public static void printArray(int[] arr) 
	{
		for(int i=0;i<arr.length;i++)
		{
			System.out.print(arr[i]+" ");
		}
		System.out.println();
		
		return;
	}
	
	//function to perform Left shift by n bits
	public static void shiftLeftByN(int[] arr, int n) 
	{
		for(int i=0;i<n;i++)
		{
			int first=arr[0];
			for(int j=1;j<arr.length;j++)
			{
				arr[j-1]=arr[j];
			}
			
			int last=arr.length-1;
			arr[last]=first;
		}
		
		return;
	}
	
	//Function to split array into 2 equal parts
	public static void splitArray(int[] bigArray, int[] leftBlock, int[] rightBlock) 
	{
		int idx=0;
		for(int i=0;i<leftBlock.length;i++)
		{
			leftBlock[i]=bigArray[idx++];
		}
		
		for(int i=0;i<rightBlock.length;i++)
		{
			rightBlock[i]=bigArray[idx++];
		}
		
		return;
	}
	
	//Function to merge array from 2 equal parts
	public static void mergeArray(int[] mergedArray, int[] leftBlock, int[] rightBlock) 
	{
		int idx=0;
		for(int i=0;i<leftBlock.length;i++)
		{
			mergedArray[idx++]=leftBlock[i];
		}
		
		for(int i=0;i<rightBlock.length;i++)
		{
			mergedArray[idx++]=rightBlock[i];
		}
		
		return;
	}
	
	public static void generateKey(int[] originalKey)
	{
		System.out.println("-------Step1 Perform P10 Permutation------");

		int[] afterP10=new int[10];
		for(int i=0;i<10;i++)
		{
			afterP10[i]=originalKey[P10[i]-1];
		}
		
		int[] leftBlock=new int[5];
		int[] rightBlock=new int[5];
		
		System.out.println("-------Step 2: Transfer into left and right blocksss------");
		splitArray(afterP10,leftBlock,rightBlock);
		
		System.out.println("-------Step 3: Perform Left-Shift by 1------");
		
		shiftLeftByN(leftBlock,1);
		shiftLeftByN(rightBlock,1);
		
		int postShiftMergedBlock[]=new int[10];
		mergeArray(postShiftMergedBlock,leftBlock,rightBlock);
		
		System.out.println("Step 4: Perform P8 to get K1");
		
		int afterP8K1[]=new int[8];
		for(int i=0;i<8;i++)
		{
			afterP8K1[i]=postShiftMergedBlock[P8[i]-1];
		}
		
		K1=afterP8K1;
		
		System.out.println("Perform LS-2 with leftBlock and rightBlock");
		
		shiftLeftByN(leftBlock, 2);
		shiftLeftByN(rightBlock, 2);
		
		System.out.println("Step 7: Perform P8 again to get K2");
		
		mergeArray(postShiftMergedBlock, leftBlock, rightBlock);
		
		int []afterP8K2=new int[8];
		for(int i=0;i<8;i++)
		{
			afterP8K2[i]=postShiftMergedBlock[P8[i]-1];
		}
		K2=afterP8K2;
		
		return;
	}
	
	//Function to perform EP (4bits-->8bits)
	public static int[] EP(int[] rightBlock) 
	{
		int[] newBlock=new int[8];
		for(int i=0;i<8;i++)
		{
			newBlock[i]=rightBlock[EP[i]-1];
		}
		
		return newBlock;
	}
	
	//Function to take XOR of 2 arrays
	public static void XOR(int[] text, int[] key) 
	{
		for(int i=0;i<key.length;i++)
		{
			if(text[i]==key[i])
			{
				text[i]=0;
			}
			else
			{
				text[i]=1;
			}
		}
		return;
	}
	
	private static int[] performS(int[] block, int[][] S) 
	{
		int row,col;
		
		//Logic to get row from 1st and 4th block bit
		if(block[0]==0 && block[3]==0)
		{
			row=0;
		}
		else if(block[0]==0 && block[3]==1)
		{
			row=1;
		}
		else if(block[0]==1 && block[3]==0)
		{
			row=2;
		}
		else
		{
			row=3;
		}
		
		//Logic to get row from 2nd and 3rd block bit
		if(block[1]==0 && block[2]==0)
		{
			col=0;
		}
		else if(block[1]==0 && block[2]==1)
		{
			col=1;
		}
		else if(block[1]==1 && block[2]==0)
		{
			col=2;
		}
		else
		{
			col=3;
		}
		
		int number=S[row][col];
		
		int[] new2BitBlock=new int[2];
		
		if(number==0)
		{
			new2BitBlock[0]=0;
			new2BitBlock[1]=0;
		}
		else if(number==1)
		{
			new2BitBlock[0]=0;
			new2BitBlock[1]=1;
		}
		else if(number==2)
		{
			new2BitBlock[0]=1;
			new2BitBlock[1]=0;
		}
		else
		{
			new2BitBlock[0]=1;
			new2BitBlock[1]=1;
		}
		
		return new2BitBlock;
	}
	
	public static int[] fK(int[] afterIP, int[] key) 
	{
		System.out.println("Step2: Split into left and right block");
		
		int[] leftBlock=new int[4];
		int[] rightBlock=new int[4];
		
		splitArray(afterIP, leftBlock, rightBlock);
		
		int[] originalLeftBlock=new int[4];
		int[] originalRightBlock=new int[4];
		
		for(int i=0;i<4;i++)
		{
			originalLeftBlock[i]=leftBlock[i];
			originalRightBlock[i]=rightBlock[i];
		}
		
		System.out.println("Step 3: Right block goes into EP to convert to 8bits.");
		
		int[] EPText=new int[8];
		
		EPText=EP(rightBlock);

		System.out.println("Step4: XOR of K1 & EPText");
		
		XOR(EPText,key);
		
		System.out.println("Step 5: Split into left & right block");
		
		splitArray(EPText, leftBlock, rightBlock);
		
		System.out.println("Step 7: Perform S0 & S1 Operations on left & right block");
		
		int []left2Bits=new int[2];
		int []right2Bits=new int[2];
		
		left2Bits=performS(leftBlock,S0);
		right2Bits=performS(rightBlock,S1);
		
		System.out.println("Merge both outputs");
		
		int []curBlock=new int[4];
		mergeArray(curBlock, left2Bits, right2Bits);
		
		System.out.println("Go for P4");
		
		int[] afterP4=new int[4];
		for(int i=0;i<4;i++)
		{
			afterP4[i]=curBlock[P4[i]-1];
		}
		
		System.out.println("Step10: XOR afterP4 and originalLeftBlock");
		XOR(afterP4, originalLeftBlock);
		
		int []finalLeftBlock=afterP4;
		int []finalRightBlock=originalRightBlock;
		
		System.out.println("Final Left Block");
		printArray(finalLeftBlock);
		
		System.out.println("Final Right Block");
		printArray(finalRightBlock);
		
		int[] finalAfterFk=new int[8];
		mergeArray(finalAfterFk, finalLeftBlock, finalRightBlock);
		printArray(finalAfterFk);
		
		return finalAfterFk;
	}

	public static int[] encrypt(int[] plainText, int[] k1, int[] k2) 
	{
		System.out.println("Step 1: Perform IP- Initial Permutation");
		
		int[] afterIP=new int[8];
		for(int i=0;i<8;i++)
		{
			afterIP[i]=plainText[IP[i]-1];
		}
		
		int []afterFk1=new int[8];
		
		System.out.println("Step2: Send to fk");
		afterFk1=fK(afterIP, k1);
		
		System.out.println("Swap internally");
		int []tempLeftBlock=new int[4];
		int []tempRightBlock=new int[4];
		
		splitArray(afterFk1, tempLeftBlock, tempRightBlock);
		
		int[] intermediateText=new int[8];
		
		mergeArray(intermediateText, tempRightBlock, tempLeftBlock);

		System.out.println("Step 4: send to fk with K2");

		int[] afterFk2=new int[8];
		afterFk2=fK(intermediateText,k2);
		
		System.out.println("Step 5: Apply IP-Inverse to get ciphertext");
		
		int[] cipherText=new int[8];
		for(int i=0;i<8;i++)
		{
			cipherText[i]=afterFk2[IP_Inverse[i]-1];
		}
		
		return cipherText;
	}
	
	public static int[] decrypt(int[] cipherText, int[] k1, int[] k2) 
	{
		System.out.println("Step 1: Perform IP- Initial Permutation");
		
		int[] afterIP=new int[8];
		for(int i=0;i<8;i++)
		{
			afterIP[i]=cipherText[IP[i]-1];
		}
		
		
		System.out.println("Step2: Send to fk");
		
		int []afterFk1=new int[8];
		afterFk1=fK(afterIP, k2);
		
		System.out.println("Swap internally");
		int []templeftBlock=new int[4];
		int []temprightBlock=new int[4];
		
		splitArray(afterFk1, templeftBlock, temprightBlock);
		
		int[] intermediateText=new int[8];
		
		mergeArray(intermediateText, temprightBlock, templeftBlock);
		
		System.out.println("Step 4: send to fk with K2");
		
		int[] afterFk2=new int[8];
		afterFk2=fK(intermediateText,k1);
		
		System.out.println("Step 5: Apply IP-Inverse to get plaintext");
		int[] originalPlainText=new int[8];
		
		for(int i=0;i<8;i++)
		{
			originalPlainText[i]=afterFk2[IP_Inverse[i]-1];
		}
		
		return originalPlainText;		
	}

	public static void main(String[] args) 
	{
		int[] key=new int[] {1,0,1,0,0,0,0,0,1,0};
		
		System.out.println("Original Key");
		printArray(key);
		
		//Step A: Generate Key
		System.out.println("-------Generate Key------");
		generateKey(key);
		
		System.out.println("---------------K1----------------");
		printArray(K1);
		System.out.println("----------------K2---------------");
		printArray(K2);
		
		//Step B: Encryption
		System.out.println("------Encrypt----------");
		
		int[] plainText=new int[] {1,0,0,1,0,1,1,1};
		int[] cipherText=new int[8];
		
		cipherText=encrypt(plainText,K1,K2);
		
		int[] originalPlainText=new int[8];
		
		//Step C: Decryption
		System.out.println("--------Decrypt----------");
		originalPlainText=decrypt(cipherText,K1,K2);
		
		System.out.println("PT:");
		printArray(plainText);
		
		System.out.println("Retrieved PT");
		printArray(originalPlainText);
	}
}

//Output
//Original Key
//1 0 1 0 0 0 0 0 1 0 
//-------Generate Key------
//-------Step1 Perform P10 Permutation------
//-------Step 2: Transfer into left and right blocksss------
//-------Step 3: Perform Left-Shift by 1------
//Step 4: Perform P8 to get K1
//Perform LS-2 with leftBlock and rightBlock
//Step 7: Perform P8 again to get K2
//---------------K1----------------
//1 0 1 0 0 1 0 0 
//----------------K2---------------
//0 1 0 0 0 0 1 1 
//------Encrypt----------
//Step 1: Perform IP- Initial Permutation
//Step2: Send to fk
//Step2: Split into left and right block
//Step 3: Right block goes into EP to convert to 8bits.
//Step4: XOR of K1 & EPText
//Step 5: Split into left & right block
//Step 7: Perform S0 & S1 Operations on left & right block
//Merge both outputs
//Go for P4
//Step10: XOR afterP4 and originalLeftBlock
//Final Left Block
//1 0 1 0 
//Final Right Block
//1 1 0 1 
//1 0 1 0 1 1 0 1 
//Swap internally
//Step 4: send to fk with K2
//Step2: Split into left and right block
//Step 3: Right block goes into EP to convert to 8bits.
//Step4: XOR of K1 & EPText
//Step 5: Split into left & right block
//Step 7: Perform S0 & S1 Operations on left & right block
//Merge both outputs
//Go for P4
//Step10: XOR afterP4 and originalLeftBlock
//Final Left Block
//0 0 1 0 
//Final Right Block
//1 0 1 0 
//0 0 1 0 1 0 1 0 
//Step 5: Apply IP-Inverse to get ciphertext
//--------Decrypt----------
//Step 1: Perform IP- Initial Permutation
//Step2: Send to fk
//Step2: Split into left and right block
//Step 3: Right block goes into EP to convert to 8bits.
//Step4: XOR of K1 & EPText
//Step 5: Split into left & right block
//Step 7: Perform S0 & S1 Operations on left & right block
//Merge both outputs
//Go for P4
//Step10: XOR afterP4 and originalLeftBlock
//Final Left Block
//1 1 0 1 
//Final Right Block
//1 0 1 0 
//1 1 0 1 1 0 1 0 
//Swap internally
//Step 4: send to fk with K2
//Step2: Split into left and right block
//Step 3: Right block goes into EP to convert to 8bits.
//Step4: XOR of K1 & EPText
//Step 5: Split into left & right block
//Step 7: Perform S0 & S1 Operations on left & right block
//Merge both outputs
//Go for P4
//Step10: XOR afterP4 and originalLeftBlock
//Final Left Block
//0 1 0 1 
//Final Right Block
//1 1 0 1 
//0 1 0 1 1 1 0 1 
//Step 5: Apply IP-Inverse to get plaintext
//PT:
//1 0 0 1 0 1 1 1 
//Retrieved PT
//1 0 0 1 0 1 1 1 
