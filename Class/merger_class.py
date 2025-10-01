from Bio import SeqIO

class Merger:
    def __init__(self, input_data: str, input_meta: str):
        self.input_file = Path(input_data)
        self.input_metafile = Path(input_meta)

    def create_database(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Extracts IDs and sequences from a FASTA file and checks for duplicates in metadata."""
        protein_ids = []
        sequences = []

        with open(self.input_file) as fasta_file:
            for seq_record in SeqIO.parse(fasta_file, "fasta"):
                protein_ids.append(seq_record.id)
                sequences.append(str(seq_record.seq))

        database = pd.DataFrame({
            "ID": protein_ids,
            "Sequence": sequences
        })

        # remove duplicates from the ID column
        database = database.drop_duplicates(subset="ID")
        
        # Load metadata
        meta_file = pd.read_csv(self.input_metafile, sep='\t')

        # Check for duplicates in Phage_ID
        duplicates = meta_file["Phage_ID"].duplicated().any()

        if duplicates:
            print("⚠️ There are duplicate Phage_ID entries in metadata!")
            meta_file = meta_file.drop_duplicates(subset="Phage_ID").reset_index(drop=True)
            print("✅ Duplicate Phage_ID entries removed from metadata!")
        else:
            print("✅ No duplicates in Phage_ID within metadata.")

        return database, meta_file

    def create_final_database(self, database: pd.DataFrame, meta_file: pd.DataFrame) -> pd.DataFrame:
        """Merges sequences and metadata into a clean final DataFrame."""

        meta_subset = meta_file[
            ['Phage_ID', 'Length', 'GC_content', 'Taxonomy', 'Completeness', 'Host',
             'Lifestyle', 'Cluster', 'Subcluster']
        ]

        data_completed = pd.merge(
            database,
            meta_subset,
            left_on="ID",
            right_on="Phage_ID",
            how="inner"
        )

        # Remove the duplicate 'Phage_ID' column
        data_completed.drop(columns='Phage_ID', inplace=True)

        # Rename the 'ID' column to 'Phage_ID'
        data_completed.rename(columns={'ID': 'Phage_ID'}, inplace=True)

        return data_completed