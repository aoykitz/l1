using System;

class Program
{
    const int SIZE = 4;
    static int[,] board1 = new int[SIZE, SIZE];
    static int[,] board2 = new int[SIZE, SIZE];

    static void Main()
    {
        StartNewGame(board1);
        StartNewGame(board2);

        bool gameOver = false;
        while (!gameOver)
        {
            Console.Clear();
            Console.WriteLine("=== Игрок 1 ===");
            PrintBoard(board1);
            Console.WriteLine("=== Игрок 2 ===");
            PrintBoard(board2);

            // Игрок 1 ход
            Console.WriteLine("Игрок 1");
            char key1 = Console.ReadKey(true).KeyChar;
            MakeMove(board1, key1);

            if (CheckSolved(board1))
            {
                Console.Clear();
                Console.WriteLine("Игрок 1 победил!");
                PrintBoard(board1);
                break;
            }

            // Игрок 2 ход
            Console.WriteLine("Игрок 2");
            char key2 = Console.ReadKey(true).KeyChar;
            MakeMove(board2, key2);

            if (CheckSolved(board2))
            {
                Console.Clear();
                Console.WriteLine("Игрок 2 победил!");
                PrintBoard(board2);
                break;
            }
        }

        Console.WriteLine("Нажмите любую клавишу для выхода...");
        Console.ReadKey();
    }

    static void StartNewGame(int[,] board)
    {
        int[] arr = GenerateSolvablePermutation();
        for (int i = 0; i < SIZE * SIZE; i++)
        {
            board[i / SIZE, i % SIZE] = arr[i];
        }
    }

    static void PrintBoard(int[,] board)
    {
        for (int r = 0; r < SIZE; r++)
        {
            for (int c = 0; c < SIZE; c++)
            {
                Console.Write(board[r, c] == 0 ? " . " : $"{board[r, c],2} ");
            }
            Console.WriteLine();
        }
    }

    static (int r, int c) FindBlank(int[,] board)
    {
        for (int r = 0; r < SIZE; r++)
            for (int c = 0; c < SIZE; c++)
                if (board[r, c] == 0) return (r, c);
        return (-1, -1);
    }

    static void MakeMove(int[,] board, char key)
    {
        var blank = FindBlank(board);
        int r = blank.r, c = blank.c;
        int newR = r, newC = c;

        switch (key)
        {
            case 'w': case 'W': newR = r - 1; break;
            case 's': case 'S': newR = r + 1; break;
            case 'a': case 'A': newC = c - 1; break;
            case 'd': case 'D': newC = c + 1; break;
            case 'i': case 'I': newR = r - 1; break;
            case 'k': case 'K': newR = r + 1; break;
            case 'j': case 'J': newC = c - 1; break;
            case 'l': case 'L': newC = c + 1; break;
            default: return;
        }

        if (newR >= 0 && newR < SIZE && newC >= 0 && newC < SIZE)
        {
            board[blank.r, blank.c] = board[newR, newC];
            board[newR, newC] = 0;
        }
    }

    static bool CheckSolved(int[,] board)
    {
        int val = 1;
        for (int r = 0; r < SIZE; r++)
            for (int c = 0; c < SIZE; c++)
            {
                int expected = (val == SIZE * SIZE) ? 0 : val;
                if (board[r, c] != expected) return false;
                val++;
            }
        return true;
    }

    static int[] GenerateSolvablePermutation()
    {
        Random rnd = new Random();
        int[] arr = new int[SIZE * SIZE];
        for (int i = 0; i < arr.Length; i++) arr[i] = i;

        do
        {
            for (int i = arr.Length - 1; i > 0; i--)
            {
                int j = rnd.Next(i + 1);
                int tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
            }
        } while (!IsSolvable(arr) || IsAlreadySolved(arr));

        return arr;
    }

    static bool IsAlreadySolved(int[] arr)
    {
        for (int i = 0; i < arr.Length - 1; i++)
            if (arr[i] != i + 1) return false;
        return arr[arr.Length - 1] == 0;
    }

    static bool IsSolvable(int[] arr)
    {
        int inversions = 0;
        for (int i = 0; i < arr.Length; i++)
            for (int j = i + 1; j < arr.Length; j++)
            {
                if (arr[i] == 0 || arr[j] == 0) continue;
                if (arr[i] > arr[j]) inversions++;
            }

        int blankIndex = Array.IndexOf(arr, 0);
        int blankRowFromTop = blankIndex / SIZE + 1;
        int blankRowFromBottom = SIZE - (blankRowFromTop - 1);

        if (SIZE % 2 == 0)
            return (blankRowFromBottom % 2 == 0) ? inversions % 2 == 1 : inversions % 2 == 0;
        else
            return inversions % 2 == 0;
    }
}
