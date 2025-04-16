import os
import boto3
from netCDF4 import Dataset

# Config AWS
AWS_REGION = "us-east-1"
S3_BUCKET_NAME = "cloudcomputing-nctf4"
LOCAL_DIR = "./tmp" 

def extract_and_save_variables(nc_path, base_filename):
    dataset = Dataset(nc_path, 'r')
    output_files = []

    for var_name in dataset.variables:
        var = dataset.variables[var_name]
        var_data = var[:]

        # Nuovo file NetCDF solo per questa variabile
        output_path = os.path.join(LOCAL_DIR, f"{var_name}.nc4")
        new_ds = Dataset(output_path, 'w', format='NETCDF4')

        # Copia le dimensioni usate dalla variabile
        for dim_name in var.dimensions:
            new_ds.createDimension(dim_name, len(dataset.dimensions[dim_name]))

        # Crea la variabile e scrive i dati
        new_var = new_ds.createVariable(var_name, var.datatype, var.dimensions)
        new_var[:] = var_data

        # Copia attributi (opzionale)
        for attr in var.ncattrs():
            setattr(new_var, attr, getattr(var, attr))

        new_ds.close()
        output_files.append((var_name, output_path))
        print(f"Variabile '{var_name}' salvata in: {output_path}")

    dataset.close()
    return output_files

def upload_to_s3(s3_client, bucket, base_filename, files):
    for var_name, path in files:
        s3_key = f"{base_filename}/{var_name}/{var_name}.nc4"
        s3_client.upload_file(path, bucket, s3_key)
        print(f"Caricato su S3: s3://{bucket}/{s3_key}")
        os.remove(path)

def main(nc_local_path):
    base_filename = os.path.basename(nc_local_path)
    s3 = boto3.client('s3', region_name=AWS_REGION)

    # Crea il bucket se non esiste
    try:
        s3.head_bucket(Bucket=S3_BUCKET_NAME)
    except:
        s3.create_bucket(Bucket=S3_BUCKET_NAME, CreateBucketConfiguration={'LocationConstraint': AWS_REGION})

    files = extract_and_save_variables(nc_local_path, base_filename)
    upload_to_s3(s3, S3_BUCKET_NAME, base_filename, files)

# === ESEMPIO USO ===
if __name__ == "__main__":
    test_url = "http://193.205.230.6/files/wrf5/d01/archive/2025/04/22/wrf5_d01_20250422Z0000.nc"
    main(test_url)